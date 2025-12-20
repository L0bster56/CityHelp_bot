from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import KeyboardButton, Message, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from config import async_session
from keyboards.start import get_main_kb
from models.users import User
from state.start import MenuForm
from manager.requests import RequestManager

router = Router()

@router.callback_query(F.data == "new_req")
async def new_req(cb: CallbackQuery, user: User, state: FSMContext):

    text = ""
    async with async_session() as session:
        req = RequestManager(session)
        text += req.list()

    await cb.message.answer(text)
