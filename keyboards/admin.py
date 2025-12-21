from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def get_main_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Добавить", callback_data="add_user_role")
    builder.button(text="Все Администраторы", callback_data="all_admin")
    builder.button(text="Все Модераторы", callback_data="all_moderator")
    builder.button(text="Все Исполнители", callback_data="all_executor")
    builder.adjust(1,3)

    return builder.as_markup(resize_keyboard=True)

def get_back_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Назад", callback_data="back_admin_ponel")

    return builder.as_markup(resize_keyboard=True)

def get_role_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Администратор", callback_data="role_admin")
    builder.button(text="Модератор", callback_data="role_moderator")
    builder.button(text="Исполнитель", callback_data="role_executor")
    builder.button(text="Гражданин", callback_data="role_user")
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
