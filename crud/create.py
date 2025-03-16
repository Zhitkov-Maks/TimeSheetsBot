from datetime import datetime

from database.db_conf import MongoDB


async def write_salary(base, earned, earned_cold, data_):
    """
    Функция для сохранения и обновления настроек пользователя.
    :param data_settings: Словарь с данными для записи.
    :return: None.
    """
    client: MongoDB = MongoDB()
    period: int = 1 if int(data_["date"][-2:]) <= 15 else 2
    parse_date = datetime.strptime(data_["date"], "%Y-%m-%d")
    user_id = data_["user_id"],
    data: dict = {
        "base_hours": float(base),
        "earned_cold": float(earned_cold),
        "earned": float(earned),
        "period": period
    }

    collection = client.get_collection("salaries")
    collection.update_one(
        {"user_id": user_id, "date": parse_date},
        {"$set": {"data": data}}, upsert=True
    )

    client.close()


async def delete_record(date: str, user_id) -> None:
    client: MongoDB = MongoDB()
    parse_date = datetime.strptime(date, "%Y-%m-%d")
    collection = client.get_collection("salaries")
    collection.delete_one({
        "user_id": user_id,
        "date": parse_date
    })
    client.close()


async def add_other_income(income: float, data: dict):
    return []


async def aggregate_data(
    year: int, month: int, user_id: int, period: int,
) -> dict:
    """
    Функция для агрегации данных за месяц и период.
    """
    client: MongoDB = MongoDB()
    collection = client.get_collection("salaries")
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month + 1, 1)
    # Пайплайн агрегации
    pipeline = [
        {
            "$match": {
                "user_id": user_id,
                "date": {"$gte": start_date, "$lt": end_date},
                "data.period": period
            }
        },
        {
            "$group": {
                "_id": None,
                "total_base_hours": {"$sum": "$data.base_hours"},
                "total_earned_cold": {"$sum": "$data.earned_cold"},
                "total_earned": {"$sum": "$data.earned"}
            }
        }
    ]

    result = collection.aggregate(pipeline).to_list()
    if len(result) != 0:
        return result[0]
    return {}
