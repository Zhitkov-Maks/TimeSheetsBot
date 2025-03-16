from database.db_conf import MongoDB


async def write_salary_shift(shifts: list[dict]) -> None:
    """
    Групповое добавление смет в базу данных.

    :param shifts: Смены пользователя.
    """
    client: MongoDB = MongoDB()
    collection = client.get_collection("salaries")
    collection.insert_many(shifts)
    client.close()
