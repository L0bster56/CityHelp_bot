from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from keyboards.start import get_main_kb, get_adress_kb
from models.users import User
from state.start import MenuForm
from manager.requests import Request
from manager.category import Category


router = Router()

@router.message(CommandStart)
async def cmd_start(message: Message, user: User, state: FSMContext):
    await state.clear()
    role = user.role
    print(role)
    await message.answer(
        f"Добро пожаловать, {message.from_user.full_name}! Выберите действие:",
        reply_markup=get_main_kb(role)
    )


