from aiogram import types


async def resend_album(message: types.Message, album: list[types.Message], chat_id: int):
    if message.text:
        await message.send_copy(chat_id=chat_id)
        return

    await message.bot.send_media_group(chat_id=chat_id, media=[
        types.InputMediaPhoto(media=m.photo[-1].file_id,
                              caption=message.caption if i == 0 else None)
        if m.photo else
        types.InputMediaVideo(media=m.video.file_id,
                              caption=message.caption if i == 0 else None)

        for i, m in enumerate(album)
        if m.photo or m.video
    ])
