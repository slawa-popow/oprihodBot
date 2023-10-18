import aiogram.types as types
from aiogram.types import WebAppInfo
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton


def get_kb_main() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton('/start'))
    return kb


def auth_kb_main() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton('/start'))
    kb.row(KeyboardButton('Добавить пользователя'))
    kb.row(KeyboardButton('Все пользователи'))
    kb.row(KeyboardButton('Забанить пользователя по id'))
    return kb

























