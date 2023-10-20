from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import User

from utils.menu_kb_gen import generate_menu_kb

router = Router()


@router.message(Command('cancel'))
async def cancel_cmd(message: types.Message, state: FSMContext, user: User):
    await state.clear()
    await message.reply('Команда отменена', reply_markup=generate_menu_kb(user.role))
