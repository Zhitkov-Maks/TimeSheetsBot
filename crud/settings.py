from database.db_conf import MongoDB


async def create_settings(data: dict, user_id: int) -> None:
    """
    Создание или обновление настроек пользователя.

    :param data: Словарь с введенными данными.
    :param user_id: Идентификатор пользователя.
    """
    client = MongoDB()
    collection = client.get_collection("users_settings")
    collection.update_one(
        {"user_id": user_id}, {"$set": data}, upsert=True
    )
    client.close()


async def get_settings_user_by_id(user_id: int) -> dict:
    """
    Получение настроек пользователя по идентификатору
    телеграм ID.
    
    :param user_id: Идентификатор телеграм.
    """
    client: MongoDB = MongoDB()
    collection = client.get_collection("users_settings")
    data = collection.find_one({"user_id": user_id})
    client.close()
    return data


async def delete_settings(user_id) -> None:
    """
    Удаление записи из бд по ID пользователя.

    :param user_id: Идентификатор пользователя.
    """
    client: MongoDB = MongoDB()
    collection = client.get_collection("users_settings")
    collection.delete_one({"user_id": user_id})
    client.close()
