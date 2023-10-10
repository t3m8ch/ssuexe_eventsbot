from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, types

from services.user_service import UserService


class UpdatingUserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[types.Update, Dict[str, Any]], Awaitable[Any]],
            update: types.Update,
            data: Dict[str, Any]
    ) -> Any:
        user_service: UserService = data['user_service']
        user = update.event.from_user
        user = await user_service.create_or_update_user(
            user_id=user.id,
            full_name=user.first_name + ((' ' + user.last_name) if user.last_name is not None else ''),
            user_name=user.username,
        )

        data['user'] = user

        return await handler(update, data)
