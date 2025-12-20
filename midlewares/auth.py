from typing import Callable, Any, Dict, Awaitable, Union


from aiogram import BaseMiddleware
from aiogram.types import Update

from config import async_session

from manager.user import UserManager

class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,

        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ):
        async with async_session() as session:
            manager = UserManager(session)
            if event.message:
                from_user = event.message.from_user
            if event.callback_query:
                from_user = event.callback_query.from_user
            user = await manager.get_or_create(
                user_id=from_user.id,
                full_name=from_user.full_name,
            )
            data["user"] = user
            return await handler(event, data)

