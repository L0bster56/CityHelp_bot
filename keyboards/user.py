from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_category_kb(categories):
    builder = InlineKeyboardBuilder()

    for category in categories:
        builder.button(
            text=f"{category.title}",
            callback_data=f"cat_{category.id}"
        )

    builder.adjust(1)
    return builder.as_markup()
