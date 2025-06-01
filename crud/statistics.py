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
        end_date = datetime(year, (month % 12) + 1, 1)
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


async def get_other_sum(
    year: int,
    month: int,
    user_id: int,
    type_operation: str
) -> dict:
    """
    Функция для агрегации данных прочих доходов/расходов за месяц.

    :param user_id: Идентификатор пользователя
    :param year: Год для выборки
    :param month: Месяц для выборки
    :param type_operation: Тип операции ('income' для доходов, иначе - расходы)
    :return: Словарь с ключом 'total_sum' и суммой, либо пустой словарь
    """
    try:
        client = MongoDB()
        collection = (
            client.get_collection("other_income")
            if type_operation == "income"
            else client.get_collection("expences")
        )

        pipeline = [
            {
                "$match": {
                    "user_id": user_id,
                    "year": year,
                    "month": month
                }
            },
            {
            "$group": {
                "_id": None,
                "total_sum": {"$sum": "$amount"}
                }
            }
        ]

        result = collection.aggregate(pipeline).to_list()

        return result[0] if result else {}
    except Exception:
        return {}
    finally:
        if client:
            client.close()
