from aiogram.fsm.state import State, StatesGroup


class ExecutorForm(StatesGroup):
    request_id = State()