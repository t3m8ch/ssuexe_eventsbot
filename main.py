from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import os
import sys
import asyncio
import logging

from handlers import event_notify


BOT_TOKEN = os.getenv('BOT_TOKEN')

dp = Dispatcher()


@dp.message(CommandStart())
async def start_cmd(message: types.Message) -> None:
    # TODO: Register user in db
    await message.answer(
        text='Hello, world!',
        reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    )


async def main() -> None:
    bot = Bot(BOT_TOKEN)
    dp.include_router(event_notify.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

