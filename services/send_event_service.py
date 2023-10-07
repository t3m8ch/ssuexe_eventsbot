from aiogram import Bot, types

from models.event_model import EventModel


class SendEventService:
    def __init__(self, bot: Bot):
        self._bot = bot

    async def send_event(self, event: EventModel, chat_id: int):
        if len(event.media) == 0:
            await self._bot.send_message(chat_id=chat_id, text=event.text)
        elif len(event.media) == 1:
            if event.media[0].media_type == 'photo':
                await self._bot.send_photo(chat_id=chat_id, photo=event.media[0].file_id, caption=event.text)
            if event.media[0].media_type == 'video':
                await self._bot.send_video(chat_id=chat_id, video=event.media[0].file_id, caption=event.text)
        else:
            await self._bot.send_media_group(chat_id=chat_id, media=[
                types.InputMediaPhoto(media=m.file_id, caption=event.text if i == 0 else None)
                if m.media_type == 'photo' else
                types.InputMediaVideo(media=m.file_id, caption=event.text if i == 0 else None)

                for i, m in enumerate(event.media)
            ])
