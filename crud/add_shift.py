from database.db_conf import MongoDB


async def add_many_shifts(shifts: list[dict]) -> None:
    """
    Групповое добавление смет в базу данных.

    :param shifts: Список со словарямя с данными для добавленяи в бд.
    """
    client: MongoDB = MongoDB()
    collection = client.get_collection("salaries")
    collection.insert_many(shifts)
    client.close()
