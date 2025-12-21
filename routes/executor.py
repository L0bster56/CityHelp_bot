from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import async_session
from keyboards.executor import req_status_edit
from keyboards.start import get_main_kb
from models.users import User
from manager.requests import RequestManager
from state.executor import ExecutorForm

router = Router()


@router.callback_query(F.data == "my_tasks")
async def my_tasks(cb: CallbackQuery, user: User, state: FSMContext):
    async with async_session() as session:
        req_manager = RequestManager(session)
        requests = await req_manager.list()

    tasks = [r for r in requests if r.status == "accepted"]

    if not tasks:
        await cb.message.edit_text(
            "У вас пока нет задач.\n",
            reply_markup=req_status_edit()
        )
        return

    text = "🛠 Мои задачи:\n\n"
    for r in tasks:
        date_str = r.created_at.strftime("%d.%m.%Y %H:%M")
        text += (
            f"🔹 Заявка №{r.id}\n"
            f"📝 {r.text}\n"
            f"📍 {r.address}\n"
            f"📅 {date_str}\n"
            f"------------------------\n"
        )

    await cb.message.edit_text(text, reply_markup=req_status_edit())


@router.callback_query(F.data == "export_tasks")
async def export_tasks(cb: CallbackQuery, state: FSMContext):
    await state.set_state(ExecutorForm.request_id)

    async with async_session() as session:
        req_manager = RequestManager(session)
        tasks = [r for r in await req_manager.list() if r.status == "accepted"]

    if not tasks:
        await cb.message.edit_text("Нет доступных задач для завершения.", reply_markup=req_status_edit())
        return

    task_list = "\n".join(f"{r.id} {r.text}" for r in tasks)
    await cb.message.edit_text(f"Введите ID выполненной заявки:\n{task_list}")


@router.message(ExecutorForm.request_id)
async def complete_task(message: Message, user: User, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Введите корректный ID заявки", reply_markup=req_status_edit())
        return

    request_id = int(message.text)

    async with async_session() as session:
        req_manager = RequestManager(session)
        task = await req_manager.get(request_id)

        if not task:
            await message.answer("❌ Заявка не найдена", reply_markup=req_status_edit())
            return
        if task.status != "accepted":
            await message.answer("⚠️ Эту заявку нельзя завершить", reply_markup=req_status_edit())
            return

        await req_manager.update_status(request_id, "done")

    await state.clear()
    await message.answer(
        f"✅ Заявка №{request_id} отмечена как выполненная!\n"
        f"Выберите действие:",
        reply_markup=get_main_kb(user.role)
    )


@router.callback_query(F.data == "back_to_reqts")
async def back_to_requests(cb: CallbackQuery, user: User, state: FSMContext):
    await cb.message.edit_text(
        f"Добро пожаловать, {cb.message.from_user.full_name}! Выберите действие:",
        reply_markup=get_main_kb(user.role)
    )
