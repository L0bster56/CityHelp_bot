from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.start import get_main_kb
from models.users import User

router = Router()


@router.message(CommandStart)
async def cmd_start(message: Message, user: User, state: FSMContext):
    await state.clear()
    role = user.role
    await message.answer(
        f"Добро пожаловать, {message.from_user.full_name}! Выберите действие:",
        reply_markup=get_main_kb(role)
    )
