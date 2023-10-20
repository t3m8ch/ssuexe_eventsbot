from uuid import UUID

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import User

from models.user_model import UserModel
from services.channel_service import ChannelService
from utils.album_resender import resend_album
from utils.channel_choosing import send_choosing_channel_message
from utils.menu_kb_gen import generate_menu_kb

router = Router()


class PostProposalStates(StatesGroup):
    choosing_channel = State()
    choosing_anon = State()
    entering_post = State()


@router.message(F.text.lower() == 'предложить пост')
async def propose_post(message: types.Message, state: FSMContext, channel_service: ChannelService):
    kb = await send_choosing_channel_message(
        fsm_context=state,
        change_state_to=PostProposalStates.choosing_channel,
        channel_service=channel_service
    )

    await message.answer(
        'Выберите канал, для которого вы хотите предложить пост, используя клавиатуру ниже',
        reply_markup=kb,
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


@router.message(F.text.startswith('/start propose_post_'))
async def propose_post_button(message: types.Message, state: FSMContext, channel_service: ChannelService):
    channel_id = message.text.split('propose_post_')[1]
    channel = await channel_service.get_channel_by_id(UUID(channel_id))

    await state.update_data(chat_id_of_chosen_channel=channel.chat_id)
    await state.update_data(channel_name=channel.name)

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


@router.message(F.text.startswith('/add_channel') & F.chat.type.in_({'group', 'supergroup'}))
async def add_channel_cmd(message: types.Message, user: UserModel, channel_service: ChannelService):
    if user.role != 'ADMIN':
        await message.reply('Эту команду имеет право использовать только администратор')
        return

    args = message.text.split()
    if len(args) < 2:
        await message.reply(
            'Вы должны указать название канала.\n'
            'Например: /add_channel КНиИТ в схемах и мемах'
        )

    channel_name = ' '.join(args[1:])
    await channel_service.add_channel(name=channel_name, chat_id=message.chat.id)

    await message.reply('Предложка добавлена!')


def _get_author_name(user: User) -> str:
    return user.full_name + (f' (@{user.username})' if user.username else '')
