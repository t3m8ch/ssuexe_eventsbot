from aiogram import Router, types
from aiogram.filters import CommandStart

from models.user_model import UserModel
from utils.menu_kb_gen import generate_menu_kb

router = Router()


@router.message(CommandStart())
async def start_cmd(message: types.Message, user: UserModel) -> None:
    await message.answer(
        text='Меню открыто',
        reply_markup=generate_menu_kb(user.role),
    )
