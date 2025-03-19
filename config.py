import os

from decouple import config


DB_NAME = os.environ.get("DB_NAME")
DB_PASS = os.environ.get("DB_PASS")
BOT_TOKEN = config("TOKEN")
