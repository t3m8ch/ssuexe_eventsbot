import asyncio
from typing import Callable, Awaitable, Any

from aiogram import types, BaseMiddleware

DEFAULT_DELAY = 0.6


class AlbumMiddleware(BaseMiddleware):
    ALBUM_DATA: dict[str, list[types.Message]] = {}

    def __init__(self, delay: int | float = DEFAULT_DELAY):
        self.delay = delay

    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: dict[str, Any],
    ) -> Any:
        if not event.media_group_id:
            if event.photo or event.video:
                data['album'] = [event]
            else:
                data['album'] = []

            return await handler(event, data)

        try:
            self.ALBUM_DATA[event.media_group_id].append(event)
            return  # Don't propagate the event
        except KeyError:
            self.ALBUM_DATA[event.media_group_id] = [event]
            await asyncio.sleep(self.delay)
            data['album'] = self.ALBUM_DATA.pop(event.media_group_id)

        return await handler(event, data)
