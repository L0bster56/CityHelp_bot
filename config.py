
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import os

from aiogram.utils.i18n import I18n

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")


engine = create_async_engine("postgresql+asyncpg://postgres:1@localhost:5432/DeliveryBot", echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)




TOKEN = os.getenv("TOKEN")


i18n = I18n(path="locales", domain="messages")

# Функция для перевода
_ = i18n.gettext

__ = lambda s: [_(s, locale="ru"),_(s, locale="en"),_(s, locale="uz")]
