
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.utils.i18n import FSMI18nMiddleware
from aiogram.client.default import DefaultBotProperties



from config import TOKEN
from midlewares.auth import AuthMiddleware
from midlewares.logging import LogingMidleware

from routes.start import router as start_handler





properties = DefaultBotProperties(
    parse_mode=ParseMode.HTML,
)

bot = Bot(TOKEN, default=properties)
dp = Dispatcher()

dp.update.middleware(LogingMidleware())
dp.update.middleware(AuthMiddleware())

dp.include_router(start_handler)

