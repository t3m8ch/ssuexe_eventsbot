from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from models.user_model import UserModel
from services.channel_service import ChannelService
from utils.menu_kb_gen import generate_menu_kb

router = Router()


class PostProposalStates(StatesGroup):
    choosing_channel = State()
    entering_post = State()


@router.message(F.text.lower() == 'предложить пост')
async def choosing_channel(message: types.Message, state: FSMContext, channel_service: ChannelService):
    channels = await channel_service.get_all_channels()

    await state.update_data(channels={channel.name:channel.chat_id for channel in channels})
    kb = [[types.KeyboardButton(text=channel.name)] for channel in channels]

    await state.set_state(PostProposalStates.choosing_channel)

    await message.answer(
        'Выберите канал, для которого вы хотите предложить пост, используя клавиатуру ниже',
        reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True),
    )


@router.message(PostProposalStates.choosing_channel)
async def entering_post(message: types.Message, state: FSMContext):
    data = await state.get_data()
    chat_id_of_chosen_channel = data['channels'].get(message.text)

    if not chat_id_of_chosen_channel:
        await message.answer('Воспользуйтесь клавиатурой ниже')
        return

    await state.update_data(chat_id_of_chosen_channel=chat_id_of_chosen_channel)

    await message.answer('Скиньте пост, который вы хотите отправить', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(PostProposalStates.entering_post)


@router.message(PostProposalStates.entering_post)
async def send_post(message: types.Message, state: FSMContext, user: UserModel):
    data = await state.get_data()
    chat_id_of_chosen_channel = data['chat_id_of_chosen_channel']

    await message.send_copy(chat_id=chat_id_of_chosen_channel)
    await message.answer('Благодарим за сотрудничество!', reply_markup=generate_menu_kb(user.role))

    await state.clear()
