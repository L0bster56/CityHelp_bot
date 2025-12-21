from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import async_session
from keyboards.user import get_category_kb
from keyboards.start import get_main_kb
from models.users import User
from state.start import MenuForm
from manager.requests import RequestManager
from manager.category import CategoryManager

router = Router()



@router.callback_query(F.data == "create_req")
async def create_req(cb: CallbackQuery, state: FSMContext):
    await state.set_state(MenuForm.for_text)
    await cb.message.edit_text("Опишите вашу проблему (минимум 10 символов):")


@router.message(MenuForm.for_text)
async def process_text(message: Message, state: FSMContext):
    if not message.text or len(message.text) < 10:
        await message.answer("Описание слишком короткое. Попробуйте еще раз.")
        return

    await state.update_data(req_text=message.text)
    await state.set_state(MenuForm.for_geo)
    await message.answer("Укажите адрес текстом или локацией:")


@router.message(MenuForm.for_geo)
async def process_geo(message: Message, state: FSMContext):
    if message.location:
        lat, lon = message.location.latitude, message.location.longitude
        address = f"Локация: {lat}, {lon}"
    elif message.text:
        address = message.text
    else:
        await message.answer("Пожалуйста, отправьте адрес текстом или локацией.")
        return

    await state.update_data(address=address)
    await state.set_state(MenuForm.for_category)

    async with async_session() as session:
        manager = CategoryManager(session)
        categories = await manager.list()

    await message.answer(
        "Выберите категорию",
        reply_markup=get_category_kb(categories)
    )


@router.callback_query(MenuForm.for_category, F.data.startswith("cat_"))
async def process_category(cb: CallbackQuery, state: FSMContext, user: User):
    category_id = int(cb.data.split("_")[1])
    data = await state.get_data()

    async with async_session() as session:
        req_manager = RequestManager(session)
        await req_manager.create(
            user_id=user.id,
            category_id=category_id,
            text=data["req_text"],
            address=data["address"]
        )

    await state.clear()
    await cb.answer("Заявка создана! ✅")
    await cb.message.edit_text(
        "✅ Ваша заявка успешно отправлена модераторам!",
        reply_markup=get_main_kb(user.role)
    )


@router.callback_query(F.data == "my_req")
async def my_req(cb: CallbackQuery, user: User):
    async with async_session() as session:
        req_manager = RequestManager(session)
        requests = await req_manager.user_list(user.id)

    if not requests:
        await cb.message.edit_text("У вас пока нет заявок.")
        return

    text = "📋 Ваши заявки:\n\n"
    for r in requests:
        date_str = r.created_at.strftime("%d.%m.%Y %H:%M")
        text += (
            f"🔹 Заявка №{r.id}\n"
            f"📝 Текст: {r.text}\n"
            f"⚙️ Статус: {r.status}\n"
            f"📅 Дата: {date_str}\n"
            f"------------------------\n"
        )

    await cb.message.edit_text(text)
