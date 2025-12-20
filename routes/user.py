from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import KeyboardButton, Message, CallbackQuery, message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from config import async_session
from keyboards.user import get_category_kb
from keyboards.start import get_main_kb
from models.users import User
from state.start import MenuForm
from manager.requests import RequestManager
from manager.category import CategoryManager

router = Router()

@router.callback_query(F.data == "create_req")
async def create_req(cb: CallbackQuery, user: User, state: FSMContext):
    await state.set_state(MenuForm.for_text)
    await cb.message.answer("Опишите вашу проблему (минимум 10 символов):")

@router.message(MenuForm.for_text)
async def process_text(message: Message, state: FSMContext):
    if not message.text or len(message.text) < 10:
        return await message.answer("Описание слишком короткое. Попробуйте еще раз.")

    await state.update_data(req_text=message.text)
    await state.set_state(MenuForm.for_geo)
    await message.answer("Укажите адрес текстом:")
    return None


@router.message(MenuForm.for_geo)
async def process_geo(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(MenuForm.for_category)

    async with async_session() as session:
        manager = CategoryManager(session)
        categories_list = await manager.list()

    await message.answer("Выберите категорию", reply_markup=get_category_kb(categories_list))



@router.callback_query(MenuForm.for_category, F.data.startswith("cat_"))
async def process_category(callback: CallbackQuery, state: FSMContext, user: User):
    category_id = int(callback.data.split("_")[1])
    data = await state.get_data()

    async with async_session() as session:
        req = RequestManager(session)
        await req.create(
            user_id=user.id,
            category_id=category_id,
            text=data['req_text'],
            address=data['address']
        )

    await state.clear()
    await callback.answer("Заявка создана!")
    await callback.message.answer(
        "✅ Ваша заявка успешно отправлена модераторам!",
        reply_markup=get_main_kb(user.role)
    )


@router.callback_query(F.data == "my_req")
async def my_req(cb: CallbackQuery, user: User, state: FSMContext):
    text = "📋 Ваши заявки:\n\n"
    async with async_session() as session:
        req = RequestManager(session)
        deta = await req.user_list(user.id)

        if not deta:
            return await cb.message.answer("У вас пока нет заявок.")

        for det in deta:

            date_str = det.created_at.strftime("%d.%m.%Y %H:%M")
            text += (
                f"🔹 **Заявка №{det.id}**\n"
                f"📝 Текст: {det.text}\n"
                f"⚙️ Статус: {det.status}\n"
                f"📅 Дата: {date_str}\n"
                f"------------------------\n"
            )

    await cb.message.answer(text)
    return None




