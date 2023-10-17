import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from handlers import event_notify, start_command, post_proposal, post_with_proposal_button
from middlewares.album_middleware import AlbumMiddleware
from middlewares.service_middleware import ServiceMiddleware
from middlewares.updating_user_middleware import UpdatingUserMiddleware
from models.base import Base

BOT_TOKEN = os.getenv('BOT_TOKEN')
SHOW_SQL = bool(os.getenv('SHOW_SQL', default=False))
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')


async def main() -> None:
    if not REDIS_HOST:
        storage = MemoryStorage()
    else:
        redis = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
        storage = RedisStorage(redis=redis)

    dp = Dispatcher(storage=storage)

    bot = Bot(BOT_TOKEN)

    engine = create_async_engine('sqlite+aiosqlite:///data/db.sqlite', echo=SHOW_SQL)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    dp.update.outer_middleware(ServiceMiddleware(session_maker))
    dp.update.outer_middleware(UpdatingUserMiddleware())
    dp.message.middleware(AlbumMiddleware())

    dp.include_router(post_proposal.router)
    dp.include_router(event_notify.router)
    dp.include_router(post_with_proposal_button.router)
    dp.include_router(start_command.router)

    await dp.start_polling(bot)

    await engine.dispose()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
