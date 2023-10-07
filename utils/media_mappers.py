from aiogram import types


class UnsupportedMediaTypeForEvent(Exception):
    pass


def map_media_message_to_dict(message: types.Message) -> dict | None:
    if message.photo:
        return dict(file_id=message.photo[-1].file_id, media_type='photo')
    if message.video:
        return dict(file_id=message.video.file_id, media_type='video')

    return None

