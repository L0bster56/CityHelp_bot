import logging
import time
from http.client import responses
from typing import Callable, Any, Dict, Awaitable, Union


from aiogram import BaseMiddleware
from aiogram.types import Update

from config import async_session

from manager.user import UserManager
from utils.logging import get_logger


class LogingMidleware(BaseMiddleware):
    async def __call__(
            self,

            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ):
        loger = get_logger()
        start_time = time.time()
        response = await handler(event, data)
        end_time = (time.time() - start_time) * 1000
        event_name = "MESSAGE" if event.message else "Callback"
        loger.info(f"{event_name} - {end_time}")
        return response