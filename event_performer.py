import asyncio
import logging
import os
import sys
from datetime import datetime

from aiogram import Bot
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from infra.broadcaster import Broadcaster
from infra.tasks_preparer import TasksPreparer
from services.event_service import EventService
from services.send_event_service import SendEventService
from services.user_service import UserService

BOT_TOKEN = os.getenv('BOT_TOKEN')
SHOW_SQL = bool(os.getenv('SHOW_SQL', default=False))
GROUPS_IDS = [int(i) for i in os.getenv('GROUPS_IDS', default='').split(',') if i != '']

now = datetime.now()


async def main():
    bot = Bot(BOT_TOKEN)

    engine = create_async_engine('sqlite+aiosqlite:///db.sqlite', echo=SHOW_SQL)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async with session_maker() as session:
        user_service = UserService(session)
        event_service = EventService(session)
        send_event_service = SendEventService(bot)

        task_preparer = TasksPreparer(GROUPS_IDS, event_service, user_service)
        tasks = await task_preparer.prepare(now)

        broadcaster = Broadcaster(tasks, event_service, send_event_service)
        await broadcaster.broadcast()

        for t in broadcaster.error_tasks:
            logging.error(f'This tasks completed with error: "{t.error_message}"')

    await engine.dispose()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
