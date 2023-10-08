import asyncio
from dataclasses import dataclass
from datetime import datetime

from services.event_service import EventService
from services.send_event_service import SendEventService

LIMIT_MESSAGES_IN_SECOND = 30
OVERLIMIT_DELAY = 1.0


@dataclass
class BroadcasterTask:
    event_id: str
    chat_id: int
    error_message: str | None = None


class Broadcaster:
    def __init__(self, tasks: list[BroadcasterTask], event_service: EventService, send_event_service: SendEventService):
        self._scheduled_tasks = tasks
        self._performed_tasks: list[BroadcasterTask] = []
        self._completed_tasks: list[BroadcasterTask] = []
        self._error_tasks: list[BroadcasterTask] = []

        self._event_service = event_service
        self._send_event_service = send_event_service

    async def broadcast(self):
        while self._scheduled_tasks:
            self._performed_tasks = self._scheduled_tasks[:LIMIT_MESSAGES_IN_SECOND]
            del self._scheduled_tasks[:LIMIT_MESSAGES_IN_SECOND]

            start = datetime.now()

            for task in self._performed_tasks:
                event = await self._event_service.get_event_by_id(task.event_id)
                try:
                    await self._send_event_service.send_event(event, task.chat_id)
                except Exception as e:
                    task.error_message = str(e)
                    self._error_tasks.append(task)
                else:
                    self._completed_tasks.append(task)

            self._performed_tasks = []

            end = datetime.now()

            delay_time = OVERLIMIT_DELAY - min(OVERLIMIT_DELAY, (start - end).total_seconds())
            await asyncio.sleep(delay_time)
