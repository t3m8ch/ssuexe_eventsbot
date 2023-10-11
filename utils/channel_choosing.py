from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StateType

from services.channel_service import ChannelService


async def send_choosing_channel_message(
        *,
        fsm_context: FSMContext,
        change_state_to: StateType,
        channel_service: ChannelService
) -> types.ReplyKeyboardMarkup:
    channels = await channel_service.get_all_channels()

    await fsm_context.update_data(channels={channel.name: channel.chat_id for channel in channels})
    await fsm_context.update_data(channels_ids={channel.name: channel.id for channel in channels})
    kb = [[types.KeyboardButton(text=channel.name)] for channel in channels]

    await fsm_context.set_state(change_state_to)

    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
