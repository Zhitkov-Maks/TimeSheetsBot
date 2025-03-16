import os

from decouple import config


DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
MONGO_URI = os.environ.get("MONGO_URI")

BOT_TOKEN = config("TOKEN")
