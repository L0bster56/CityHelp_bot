from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def req_status_edit():
    builder = InlineKeyboardBuilder()

    builder.button(text="Назад", callback_data="back_to_reqts")


    return builder.as_markup(resize_keyboard=True)


