from aiogram import types


async def resend_album(message: types.Message, album: list[types.Message], chat_id: int):
    if message.text:
        await message.send_copy(chat_id=chat_id)
        return

    media = []
    for i, m in enumerate(album):
        caption = message.caption if i == 0 else None

        if m.photo:
            media.append(types.InputMediaPhoto(media=m.photo[-1].file_id, caption=caption))
        elif m.video:
            media.append(types.InputMediaVideo(media=m.video.file_id, caption=caption))
        elif m.document:
            media.append(types.InputMediaDocument(media=m.document.file_id, caption=caption))
        elif m.audio:
            media.append(types.InputMediaAudio(media=m.audio.file_id, caption=caption))

    await message.bot.send_media_group(chat_id=chat_id, media=media)
