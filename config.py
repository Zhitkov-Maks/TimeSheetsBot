import os

from aiogram import Bot

from decouple import config


DB_NAME = os.environ.get("DB_NAME")
DB_PASS = os.environ.get("DB_PASS")
BOT_TOKEN = config("TOKEN")


bot = Bot(token=BOT_TOKEN)
cashed_currency = {}
