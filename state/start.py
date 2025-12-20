from aiogram.fsm.state import State, StatesGroup


class MenuForm(StatesGroup):
    for_text = State()
    for_category = State()
    for_geo = State()