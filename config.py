from decouple import config

import os

from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

BOT_TOKEN = config("TOKEN")

weekdays = ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")
app_schedule: dict = {}
scheduler_ids: dict = {}
