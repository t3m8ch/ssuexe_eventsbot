from datetime import datetime, timedelta

from infra.broadcaster import BroadcasterTask
from services.event_service import EventService
from services.user_service import UserService


class TasksPreparer:
    def __init__(self, groups_ids: list[int], event_service: EventService, user_service: UserService):
        self._groups_ids = groups_ids
        self._event_service = event_service
        self._user_service = user_service

    async def prepare(self, current_time: datetime) -> list[BroadcasterTask]:
        from_time = current_time.replace(second=0, microsecond=0)
        to_time = from_time + timedelta(seconds=59)

        tasks = []

        events = await self._event_service.get_events_with_datetime(from_time, to_time)
        for e in events:
            users = await self._user_service.get_users()
            chats_ids = self._groups_ids + [u.id for u in users]
            for c in chats_ids:
                tasks.append(BroadcasterTask(event_id=e.id, chat_id=c))

        return tasks
