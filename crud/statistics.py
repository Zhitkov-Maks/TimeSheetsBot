from datetime import datetime

from database.db_conf import MongoDB


async def get_information_for_month(
    user_id: int,
    year: int,
    month: int
) -> list:
    """
    Получение данных за выбранный месяц. Эти данные нужны для
    отображения в календаре.

    :param user_id: Идентификатор пользователя.
    :param year: Переданный год.
    :param month: Переданный месяц.
    """
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
    Функция возвращает данные за конкретную выбранную дату.

    :param user_id: Идентификатор пользователя.
    :param date: Конкретная дата для показа пользователю.
    """
    client: MongoDB = MongoDB()
    parse_date = datetime.strptime(date, "%Y-%m-%d")
    collection = client.get_collection("salaries")
    data: dict = collection.find_one({"user_id": user_id, "date": parse_date})
    client.close()
    return data


async def aggregate_data_worked_hours(
    year: int,
    month: int,
    user_id: int
) -> dict:
    """
    Функция для получения отработанных часов за месяц. Эти данные 
    нужны при вычислении ожидаемой зп, для вычисления разного рода доплат.

    :param user_id: Идентификатор пользователя.
    :param year: Переданный год.
    :param month: Переданный месяц.
    """
    client: MongoDB = MongoDB()
    collection = client.get_collection("salaries")
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month + 1, 1)
    pipeline = [
        {
            "$match": {
                "user_id": user_id,
                "date": {"$gte": start_date, "$lt": end_date},
            }
        },
        {
            "$group": {
                "_id": None,
                "total_base_hours": {"$sum": "$base_hours"}
            }
        }
    ]
    result = collection.aggregate(pipeline).to_list()
    if len(result) != 0:
        return result[0]
    return {}


async def aggregate_data(
    year: int, month: int, user_id: int, period: int,
) -> dict:
    """
    Функция для агрегации данных за месяц и период. Вычисляется сумма 
    отработанных часов за период и сумма оплаты за часы.

    :param user_id: Идентификатор пользователя.
    :param year: Переданный год.
    :param month: Переданный месяц.
    :param period: 1-й или 2-й периоды.
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
                "period": period
            }
        },
        {
            "$group": {
                "_id": None,
                "total_base_hours": {"$sum": "$base_hours"},
                "total_earned": {"$sum": "$earned"},
                "total_earned_hours": {"$sum": "$earned_hours"},
                "total_earned_cold": {"$sum": "$earned_cold"},
            }
        }
    ]

    result = collection.aggregate(pipeline).to_list()
    if len(result) != 0:
        return result[0]
    return {}
