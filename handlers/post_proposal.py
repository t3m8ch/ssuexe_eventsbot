from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import User

from models.user_model import UserModel
from services.channel_service import ChannelService
from utils.album_resender import resend_album
from utils.menu_kb_gen import generate_menu_kb

router = Router()


class PostProposalStates(StatesGroup):
    choosing_channel = State()
    choosing_anon = State()
    entering_post = State()


@router.message(F.text.lower() == 'предложить пост')
async def propose_post(message: types.Message, state: FSMContext, channel_service: ChannelService):
    channels = await channel_service.get_all_channels()

    await state.update_data(channels={channel.name: channel.chat_id for channel in channels})
    kb = [[types.KeyboardButton(text=channel.name)] for channel in channels]

    await state.set_state(PostProposalStates.choosing_channel)

    await message.answer(
        'Выберите канал, для которого вы хотите предложить пост, используя клавиатуру ниже',
        reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True),
    )


@router.message(PostProposalStates.choosing_channel)
async def choose_channel(message: types.Message, state: FSMContext):
    data = await state.get_data()
    chat_id_of_chosen_channel = data['channels'].get(message.text)

    if not chat_id_of_chosen_channel:
        await message.answer('Воспользуйтесь клавиатурой ниже')
        return

    await state.update_data(chat_id_of_chosen_channel=chat_id_of_chosen_channel)
    await state.update_data(channel_name=message.text)

    kb = [
        [types.KeyboardButton(text='Да, я хочу, чтобы меня упомянули, как автора')],
        [types.KeyboardButton(text='Нет, я хочу остаться анонимным')],
    ]
    await message.answer('Хотите ли вы, чтобы вас упомянули, как автора, при публикации?',
                         reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))

    await state.set_state(PostProposalStates.choosing_anon)


@router.message(PostProposalStates.choosing_anon)
async def choosing_anon(message: types.Message, state: FSMContext):
    if message.text == 'Да, я хочу, чтобы меня упомянули, как автора':
        await state.update_data(is_anon=False)
    elif message.text == 'Нет, я хочу остаться анонимным':
        await state.update_data(is_anon=True)
    else:
        await message.answer('Воспользуйтесь клавиатурой ниже')
        return

    await message.answer('Скиньте пост, который вы хотите отправить',
                         reply_markup=types.ReplyKeyboardRemove())

    await state.set_state(PostProposalStates.entering_post)


@router.message(PostProposalStates.entering_post)
async def send_post(message: types.Message, album: list[types.Message], state: FSMContext, user: UserModel):
    data = await state.get_data()
    chat_id_of_chosen_channel = data['chat_id_of_chosen_channel']

    author_name = _get_author_name(message.from_user)
    if data['is_anon']:
        text = (
            f'Отправлен пост для канала "{data["channel_name"]}"\n\n'
            'Человек попросил остаться анонимным'
        )
    else:
        text = (
            f'{author_name} отправил пост для канала "{data["channel_name"]}"\n\n'
            'Человек попросил указать авторство'
        )

    await message.bot.send_message(
        chat_id=chat_id_of_chosen_channel,
        text=text
    )

    await resend_album(message, album, chat_id_of_chosen_channel)
    await message.answer('Благодарим за сотрудничество!', reply_markup=generate_menu_kb(user.role))

    await state.clear()


def _get_author_name(user: User) -> str:
    return user.full_name + (f' (@{user.username})' if user.username else '')
