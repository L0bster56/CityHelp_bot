from aiogram.fsm.state import State, StatesGroup


class ModerForm(StatesGroup):
    request_id = State()