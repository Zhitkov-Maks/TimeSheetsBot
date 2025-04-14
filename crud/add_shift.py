import pymongo

from database.db_conf import MongoDB


async def add_many_shifts(shifts: list[dict]) -> None:
    """
    Групповое добавление смет в базу данных.

    :param shifts: Список со словарямя с данными для добавленяи в бд.
    """
    client: MongoDB = MongoDB()
    collection = client.get_collection("salaries")

    # Создаем уникальный индекс (если его еще нет)
    collection.create_index(
        [("user_id", 1), ("date", 1)],
        unique=True,
        name="unique_user_date"
    )
    try:
        collection.insert_many(shifts)
    except pymongo.errors.DuplicateKeyError:
        pass
    finally:
        client.close()
