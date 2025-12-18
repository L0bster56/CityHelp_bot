from aiogram import Router, F
from aiogram.filters import or_f
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message,CallbackQuery

from keyboards.start import get_start_kb
from models.users import User

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, user: User, state: FSMContext):
    await state.clear()
    print(user.full_name)

    await message.answer("Привет я интернет Магазин \nВыберите действия", reply_markup=get_start_kb(user.language))


@router.callback_query(F.data == "back")
async def start_handler_back(callback: CallbackQuery,user: User, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "Выберите действия",
        reply_markup=get_start_kb(user.language)
    )