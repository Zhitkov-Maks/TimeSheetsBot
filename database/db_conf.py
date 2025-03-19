"""We describe the connection to the database."""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from config import DB_NAME, DB_PASS


MONGO_URI = f"mongodb://{DB_NAME}:{DB_PASS}@mongodb"


class MongoDB:
    def __init__(self):
        if not isinstance(DB_NAME, str):
            raise ValueError("DB_NAME must be a string")

        try:
            self.client = MongoClient(MONGO_URI)
            self.db = self.client[DB_NAME]
        except ConnectionFailure as e:
            raise

    def get_collection(self, collection_name: str):
        return self.db[collection_name]

    def close(self):
        self.client.close()
