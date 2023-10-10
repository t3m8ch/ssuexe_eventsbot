from typing import Callable, Dict, Any, Awaitable

import aiosqlite
from aiogram import BaseMiddleware, types
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from services.event_service import EventService
from services.user_service import UserService


class ServiceMiddleware(BaseMiddleware):
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self._session_maker = session_maker

    async def __call__(
            self,
            handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: types.TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        async with self._session_maker() as session:
            data['user_service'] = UserService(session)
            data['event_service'] = EventService(session)
            return await handler(event, data)
