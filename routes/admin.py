from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import async_session
from keyboards.admin import get_main_kb, get_back_kb, get_role_kb
from models.users import User
from state.admin import AdminForm
from manager.user import UserManager

router = Router()


@router.callback_query(F.data.in_(["my_admin", "back_admin_ponel"]))
async def admin_panel(cb: CallbackQuery, user: User, state: FSMContext):
    await state.clear()
    await cb.message.edit_text("Что нужно сделать", reply_markup=get_main_kb())



async def send_users_by_role(cb: CallbackQuery, role: str, title: str):
    text = f"Все {title}\n\n"
    async with async_session() as session:
        manager = UserManager(session)
        users = await manager.list()
    for u in users:
        if u.role == role:
            text += f"{u.full_name} - {u.id}\n"
    await cb.message.edit_text(text, reply_markup=get_back_kb())


@router.callback_query(F.data == "all_admin")
async def get_admins(cb: CallbackQuery):
    await send_users_by_role(cb, "admin", "Администраторы")


@router.callback_query(F.data == "all_moderator")
async def get_moderators(cb: CallbackQuery):
    await send_users_by_role(cb, "moderator", "Модераторы")


@router.callback_query(F.data == "all_executor")
async def get_executors(cb: CallbackQuery):
    await send_users_by_role(cb, "executor", "Исполнители")


@router.callback_query(F.data == "add_user_role")
async def add_user_role(cb: CallbackQuery, state: FSMContext):
    await state.set_state(AdminForm.user_id)
    await cb.message.edit_text("Введите ID пользователя", reply_markup=get_back_kb())


@router.message(AdminForm.user_id)
async def enter_user_id(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("ID должен быть числом")
        return

    await state.update_data(user_id=int(message.text))
    await state.set_state(AdminForm.user_role)
    await message.answer("Выберите роль:", reply_markup=get_role_kb())


@router.callback_query(AdminForm.user_role)
async def set_user_role(cb: CallbackQuery, state: FSMContext):
    user_role = cb.data.split("_")[1]
    data = await state.get_data()

    async with async_session() as session:
        manager = UserManager(session)
        await manager.update_role(user_id=data["user_id"], role=user_role)

    await state.clear()
    await cb.answer("Успешно ✅")
    await cb.message.edit_text("Что нужно сделать", reply_markup=get_main_kb())
