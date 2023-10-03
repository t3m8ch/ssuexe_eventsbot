from aiogram import Router, types
from aiogram.filters import CommandStart

from services.user_service import UserService
from utils.menu_kb_gen import generate_menu_kb

router = Router()


@router.message(CommandStart())
async def start_cmd(message: types.Message, user_service: UserService) -> None:
    user = await user_service.get_user_by_id(message.from_user.id)
    await message.answer(
        text='Hello, world!',
        reply_markup=generate_menu_kb(user.role),
    )
