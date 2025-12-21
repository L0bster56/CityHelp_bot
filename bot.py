from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.utils.i18n import FSMI18nMiddleware
from aiogram.client.default import DefaultBotProperties



from config import TOKEN
from midlewares.auth import AuthMiddleware
from midlewares.logging import LogingMidleware

from routes.menu import router as start_handler
from routes.user import router as user_router
from routes.admin import router as admin_router
from routes.moder import router as moderator_router
from routes.executor import router as executor_router






properties = DefaultBotProperties(
    parse_mode=ParseMode.HTML,
)

bot = Bot(TOKEN, default=properties)
dp = Dispatcher()

dp.update.middleware(LogingMidleware())
dp.update.middleware(AuthMiddleware())


dp.include_router(user_router)
dp.include_router(executor_router)
dp.include_router(moderator_router)
dp.include_router(admin_router)
dp.include_router(start_handler)



