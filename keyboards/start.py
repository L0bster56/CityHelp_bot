from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_start_kb(language):
    builder = InlineKeyboardBuilder()

    builder.button(text="🔍 Заказать", callback_data="menu")
    builder.button(text="📚 История Заказов", callback_data="history")
    builder.button(text="👥 О нас", callback_data="about")
    builder.button(text="⚙️ Настройки", callback_data="settings")

    builder.adjust(1, 3)
    return builder.as_markup()


def get_back(language):
    builder = InlineKeyboardBuilder()
    builder.button(text="Назад", callback_data="back")
    return builder.as_markup()