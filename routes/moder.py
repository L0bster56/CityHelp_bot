from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import async_session
from keyboards.moder import req_status_edit, req_status
from keyboards.start import get_main_kb
from models.users import User
from manager.requests import RequestManager
from state.moder import ModerForm

router = Router()



@router.callback_query(F.data == "new_req")
async def show_new_requests(cb: CallbackQuery, user: User, state: FSMContext):
    async with async_session() as session:
        req_manager = RequestManager(session)
        requests = await req_manager.list()

    new_requests = [r for r in requests if r.status == "new"]

    if not new_requests:
        await cb.message.edit_text("Новых заявок нет.", reply_markup=req_status())
        return

    text = "🆕 Новые заявки:\n\n"
    for r in new_requests:
        date_str = r.created_at.strftime("%d.%m.%Y %H:%M")
        text += (
            f"🔹 Заявка №{r.id}\n"
            f"👤 Пользователь ID: {r.user_id}\n"
            f"📝 {r.text}\n"
            f"📍 {r.address}\n"
            f"📅 {date_str}\n"
            f"------------------------\n"
        )

    await cb.message.edit_text(text, reply_markup=req_status_edit())


@router.callback_query(F.data == "req_status_edit")
async def ask_request_id(cb: CallbackQuery, state: FSMContext):
    await state.set_state(ModerForm.request_id)
    await cb.message.answer("Введите ID заявки для принятия:")


@router.message(ModerForm.request_id)
async def accept_request(message: Message, user: User, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("ID должен быть числом", reply_markup=req_status())
        return

    request_id = int(message.text)
    async with async_session() as session:
        req_manager = RequestManager(session)
        request = await req_manager.get(request_id)

        if not request:
            await message.answer("Заявка не найдена", reply_markup=req_status())
            return
        if request.status != "new":
            await message.answer("Эта заявка уже обработана", reply_markup=req_status())
            return

        await req_manager.update_status(request_id, "accepted")

    await state.clear()
    await message.answer(
        f"✅ Заявка принята, {message.from_user.full_name}! Выберите действие:",
        reply_markup=get_main_kb(user.role)
    )



@router.callback_query(F.data == "all_req")
async def all_requests(cb: CallbackQuery, user: User, state: FSMContext):
    async with async_session() as session:
        req_manager = RequestManager(session)
        requests = await req_manager.list()

    text = "📋 Все заявки:\n\n"
    for r in requests:
        date_str = r.created_at.strftime("%d.%m.%Y %H:%M")
        text += (
            f"🔹 Заявка №{r.id}\n"
            f"👤 Пользователь ID: {r.user_id}\n"
            f"📝 {r.text}\n"
            f"📍 {r.address}\n"
            f"⚙️ {r.status}\n"
            f"📅 {date_str}\n"
            f"------------------------\n"
        )

    await cb.message.edit_text(text, reply_markup=req_status())



@router.callback_query(F.data == "back_to_req")
async def back_to_req(cb: CallbackQuery, user: User, state: FSMContext):
    await cb.message.answer(
        f"Добро пожаловать, {cb.message.from_user.full_name}! Выберите действие:",
        reply_markup=get_main_kb(user.role)
    )
