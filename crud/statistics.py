from datetime import datetime

from database.db_conf import MongoDB


async def get_information_for_month(
    user_id: int,
    year: int,
    month: int
) -> list:
    try:
        client: MongoDB = MongoDB()
        collection = client.get_collection("salaries")
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month + 1, 1)
        cursor = collection.find(
            {
                "user_id": user_id,
                "date": {"$gte": start_date, "$lt": end_date},
            }
        )
        results = cursor.to_list(length=None)
        return results
    finally:
        client.close()


async def get_info_by_date(user_id: int, date: str) -> dict:
    """
    Функция возвращает данные за выбранную дату.
    """
    client: MongoDB = MongoDB()
    parse_date = datetime.strptime(date, "%Y-%m-%d")
    collection = client.get_collection("salaries")
    data: dict = collection.find_one({"user_id": user_id, "date": parse_date})
    client.close()
    return data
