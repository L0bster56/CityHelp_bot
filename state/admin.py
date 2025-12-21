from aiogram.fsm.state import State, StatesGroup


class AdminForm(StatesGroup):
    user_id = State()
    user_role = State()