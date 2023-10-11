from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from models.user_model import UserModel
from services.channel_service import ChannelService
from utils.channel_choosing import send_choosing_channel_message
from utils.menu_kb_gen import generate_menu_kb


class CreatingPostWithProposalButtonStates(StatesGroup):
    choosing_channel = State()
    entering_text = State()
    pin_photo = State()


router = Router()


@router.message(Command('proposal_button'))
async def create_post_with_proposal_button_cmd(
        message: types.Message,
        state: FSMContext,
        channel_service: ChannelService
):
    kb = await send_choosing_channel_message(
        fsm_context=state,
        change_state_to=CreatingPostWithProposalButtonStates.choosing_channel,
        channel_service=channel_service
    )

    await message.answer(
        'Выберите канал, для которого вы хотите сделать пост',
        reply_markup=kb,
    )


@router.message(CreatingPostWithProposalButtonStates.choosing_channel)
async def propose_post(message: types.Message, state: FSMContext):
    data = await state.get_data()
    channel_id = data['channels_ids'].get(message.text)

    if not channel_id:
        await message.answer('Воспользуйтесь клавиатурой ниже')
        return

    await state.update_data(channel_id=channel_id)

    await message.answer(
        'Введите текст, который будет у поста. Размер текста не должен привышать 500 символов',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(CreatingPostWithProposalButtonStates.entering_text)


@router.message(CreatingPostWithProposalButtonStates.entering_text)
async def entering_text(message: types.Message, state: FSMContext):
    if len(message.text) > 500:
        await message.answer('Размер текста не должен привышать 500 символов')
        return

    await state.update_data(text=message.text)

    await message.answer(
        'Отправьте фотографию, которую вы хотите прикрепить посту',
        reply_markup=types.ReplyKeyboardMarkup(keyboard=[
            [types.KeyboardButton(text='Не прикреплять фотографию')]
        ], resize_keyboard=True)
    )

    await state.set_state(CreatingPostWithProposalButtonStates.pin_photo)


@router.message(CreatingPostWithProposalButtonStates.pin_photo, (F.text == 'Не прикреплять фотографию') | F.photo)
async def pin_photo(message: types.Message, state: FSMContext, user: UserModel):
    data = await state.get_data()
    me = await message.bot.me()

    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text='Предложить пост',
            url=f'https://t.me/{me.username}?start=propose_post_{data["channel_id"]}'
        )]
    ])

    await message.answer('Пост готов', reply_markup=generate_menu_kb(user.role))

    if message.text == 'Не прикреплять фотографию':
        await message.answer(text=data['text'], reply_markup=kb)
    else:
        await message.answer_photo(photo=message.photo[-1].file_id, caption=data['text'], reply_markup=kb)

    await state.clear()
