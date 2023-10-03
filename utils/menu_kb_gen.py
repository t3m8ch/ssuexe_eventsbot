from aiogram import types

from common.types import UserRole


def generate_menu_kb(user_role: UserRole) -> types.ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text='Предложить пост')]
    ]

    if user_role == 'ADMIN':
        kb.append([types.KeyboardButton(text='Уведомить о событии')])

    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
