from database.db_conf import MongoDB

import pymongo


async def get_salary_for_day(day_id: str) -> None:
    """
    Функция для получения данных за день.

    :param daн_id: Идентификатор записи.
    """
    try:
        client = MongoDB()
        collection = client.get_collection("salaries")
        data: dict = collection.find_one({"_id": day_id})
        return data
    finally:
        client.close()


async def update_salary(
    day_id: int, data: dict
) -> None:
    """
    Функция обновления зарплаты за день.

    :param day_id: Идентификатор дня.
    :param data: Словарь с данными для записи.
    """
    client: MongoDB = MongoDB()
    collection = client.get_collection("salaries")

    try:
        collection.update_one(
            {"_id": day_id},
            {"$set": data},
            upsert=True
        )
    except pymongo.errors.DuplicateKeyError:
        pass
    finally:
        client.close()
