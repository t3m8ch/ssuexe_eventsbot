import os
from datetime import datetime

import aiosqlite
from aiogram import Bot

from infra.broadcaster import Broadcaster
from infra.tasks_preparer import TasksPreparer
from services.event_service import EventService
from services.send_event_service import SendEventService
from services.user_service import UserService

BOT_TOKEN = os.getenv('BOT_TOKEN')
GROUPS_IDS = list(map(int, os.getenv('GROUPS_IDS').split(',')))

now = datetime.now()


async def main():
    bot = Bot(BOT_TOKEN)

    async with aiosqlite.connect('db.sqlite') as connection:
        user_service = UserService(connection)
        event_service = EventService(connection)
        send_event_service = SendEventService(bot)

        task_preparer = TasksPreparer(GROUPS_IDS, event_service, user_service)
        tasks = await task_preparer.prepare(now)

        broadcaster = Broadcaster(tasks, event_service, send_event_service)
        await broadcaster.broadcast()


if __name__ == '__main__':
    print('Perform events')
