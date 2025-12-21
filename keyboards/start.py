from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def get_main_kb(role: str):
    builder = InlineKeyboardBuilder()


    if role == 'user':
        builder.button(text="📝 Создать заявку", callback_data="create_req")
        builder.button(text="📋 Мои заявки", callback_data="my_req")

    elif role == 'moderator':
        builder.button(text="🔍 Новые заявки",callback_data="new_req")
        builder.button(text="📊 Все заявки", callback_data="all_req")

    elif role == 'executor':
        builder.button(text="🛠 Мои задачи", callback_data="my_tasks")
        builder.button(text="✅ Отправить отчет", callback_data="export_tasks")

    elif role == 'admin':
        builder.button(text="👥 Управление пользователями", callback_data="my_admin")

    return builder.as_markup(resize_keyboard=True)


def get_adress_kb():
    kb = ReplyKeyboardBuilder()
    kb.add(KeyboardButton(text="📍 Отправить локацию", request_location=True))
    kb.add(KeyboardButton(text="Пропустить"))


def get_category_kb(all_categories):
    builder = InlineKeyboardBuilder()
    for cat in all_categories:
        builder.add(InlineKeyboardButton(
            text=cat.title,
            callback_data=f"cat_{cat.id}")
        )
    builder.adjust(1)


