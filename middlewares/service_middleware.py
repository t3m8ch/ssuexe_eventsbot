from typing import Callable, Dict, Any, Awaitable

import aiosqlite
from aiogram import BaseMiddleware, types

from services.user_service import UserService


class ServiceMiddleware(BaseMiddleware):
    def __init__(self, db: aiosqlite.Connection):
        self._db = db

    async def __call__(
            self,
            handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: types.TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        data['user_service'] = UserService(self._db)
        return await handler(event, data)
