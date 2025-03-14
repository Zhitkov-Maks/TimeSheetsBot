from typing import Dict

from database.db_conf import MongoDB


async def write_settings(data_settings: Dict[str, str | int]) -> None:
    """
    Функция для сохранения и обновления настроек пользователя.
    :param data_settings: Словарь с данными для записи.
    :return: None.
    """
    client: MongoDB = MongoDB()
    collection = client.get_collection("users_settings")
    print(data_settings)
    collection.insert_one(data_settings)
