import aiosqlite
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import os
import sys
import asyncio
import logging

from db_init import init_db
from handlers import event_notify, start_command
from middlewares.service_middleware import ServiceMiddleware
from middlewares.updating_user_middleware import UpdatingUserMiddleware

BOT_TOKEN = os.getenv('BOT_TOKEN')

dp = Dispatcher()


async def main() -> None:
    bot = Bot(BOT_TOKEN)

    async with aiosqlite.connect('db.sqlite') as connection:
        await init_db(connection)

        dp.update.outer_middleware(ServiceMiddleware(connection))
        dp.update.outer_middleware(UpdatingUserMiddleware())

        dp.include_router(start_command.router)
        dp.include_router(event_notify.router)

        await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
