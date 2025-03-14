"""We describe the connection to the database."""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGO_URI = "mongodb://maxi_salary_bot:44565vfrc@localhost:27017/"
DB_NAME = "maxi_salary_bot"


class MongoDB:
    def __init__(self):
        if not isinstance(DB_NAME, str):
            raise ValueError("DB_NAME must be a string")

        try:
            self.client = MongoClient(MONGO_URI)
            self.client.admin.command("ping")  # Проверка подключения
            self.db = self.client[DB_NAME]
            logger.info("Успешное подключение к MongoDB")
        except ConnectionFailure as e:
            logger.error(f"Ошибка подключения к MongoDB: {e}")
            raise

    def get_collection(self, collection_name: str):
        return self.db[collection_name]

    def close(self):
        self.client.close()
        logger.info("Соединение с MongoDB закрыто")
