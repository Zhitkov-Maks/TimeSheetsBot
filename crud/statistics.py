from datetime import datetime
from dateutil.relativedelta import relativedelta

from database.db_conf import MongoDB


async def get_other_incomes_for_year(
    user_id: int,
    year: int
) -> list:
    """
    Get other data for the selected year.

    :param user_id: The user's ID.
    :param year: The transmitted year.
    """
    try:
        client: MongoDB = MongoDB()
        collection = client.get_collection("other_income")
        pipeline = [
            {
                "$match": {
                    "user_id": user_id,
                    "year": year
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_other_amount": {"$sum": "$amount"}
                }
            }
        ]

        result = collection.aggregate(pipeline).to_list()
        if len(result) != 0:
            return result[0]
        return {}
    finally:
        client.close()


async def get_other_incomes_expenses(
    user_id: int,
    year: int,
    month: int,
    income: bool
) -> list:
    """
    Get other data for the selected month.

    :param user_id: The user's ID.
    :param year:    The transmitted year.
    :param month: The transferred month.
    """
    type_ = "other_income" if income else "expences"
    try:
        client: MongoDB = MongoDB()
        collection = client.get_collection(type_)
        cursor = collection.find(
            {
                "user_id": user_id,
                "year": year,
                "month": month
            }
        )
        results = cursor.to_list(length=None)
        return results
    finally:
        client.close()


async def get_information_for_month(
    user_id: int,
    year: int,
    month: int
) -> list:
    """
    Get the data for the selected month.

    :param user_id: The user's ID.
    :param year: The transmitted year.
    :param month: The transferred month.
    """
    try:
        client: MongoDB = MongoDB()
        collection = client.get_collection("salaries")
        start_date = datetime(year, month, 1)
        end_date = start_date + relativedelta(months=1)
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
    Get the data for a specific selected date.

    :param user_id: The user's ID.
    :param date: A specific date to show to the user.
    """
    try:
        client: MongoDB = MongoDB()
        parse_date = datetime.strptime(date, "%Y-%m-%d")
        collection = client.get_collection("salaries")
        data: dict = collection.find_one(
            {"user_id": user_id, "date": parse_date}
        )
        return data
    finally:
        client.close()


async def statistics_for_year(year: int, user_id: int) -> dict:
    """
    Aggregate the data for the year.

    :param user_id: The user's ID.
    :param year: The transmitted year.
    """
    try:
        client: MongoDB = MongoDB()
        collection = client.get_collection("salaries")
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1)

        pipeline = [
            {
                "$match": {
                    "user_id": user_id,
                    "date": {"$gte": start_date, "$lt": end_date}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_hours": {"$sum": "$base_hours"},
                    "total_earned": {"$sum": "$earned"},
                    "total_award": {"$sum": "$award_amount"},
                    "dollar": {"$sum": "$valute.dollar"},
                    "euro": {"$sum": "$valute.euro"},
                    "yena": {"$sum": "$valute.yena"},
                    "som": {"$sum": "$valute.som"}
                }
            },
            {
                "$project": {
                    "total_hours": {"$round": ["$total_hours", 2]},
                    "total_earned": {"$round": ["$total_earned", 2]},
                    "total_award": {"$round": ["$total_award", 2]},
                    "dollar": {"$round": ["$dollar", 2]},
                    "euro": {"$round": ["$euro", 2]},
                    "yena": {"$round": ["$yena", 2]},
                    "som": {"$round": ["$som", 2]}
                }
            }
        ]

        result = collection.aggregate(pipeline).to_list()
        if len(result) != 0:
            return result[0]
        return {}
    finally:
        client.close()


async def aggregate_data(
    year: int, month: int, user_id: int, period: int,
) -> dict:
    """
    Calculate the amount of hours worked for the period 
    and the amount of payment for the hours.

    :param user_id: The user's ID.
    :param year: The transmitted year.
    :param month: The transferred month.
    :param period: 1st or 2nd periods.
    """
    try:
        client: MongoDB = MongoDB()
        collection = client.get_collection("salaries")
        start_date = datetime(year, month, 1)
        end_date = start_date + relativedelta(months=1)

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
                    "total_award": {"$sum": "$award_amount"},
                    "total_operations": {"$sum": "$count_operations"},
                    "total_overitme": {"$sum": "$earned_overtime"},
                    "total_hours_overitme": {"$sum": "$hours_overtime"},
                }
            }
        ]

        result = collection.aggregate(pipeline).to_list()
        if len(result) != 0:
            return result[0]
        return {}
    finally:
        client.close()


async def get_other_sum(
    year: int,
    month: int,
    user_id: int,
    type_operation: str
) -> dict:
    """
    Aggregate the data on other income/expenses for the month.

    :param user_id: User ID.
    :param year: Year for the sample.
    :param month: The month for the sample.
    :param type_operation: Type of operation 
                            ('income' for income, otherwise - expenses)
    :return: A dictionary with the key 'total_sum' and the sum, 
                or an empty dictionary
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


async def aggregate_valute(
    year: int, month: int, user_id: int
) -> dict:
    """
    Calculate the amount of hours worked for the period 
    and the amount of payment for the hours.

    :param user_id: The user's ID.
    :param year: The transmitted year.
    :param month: The transferred month.
    """
    try:
        client: MongoDB = MongoDB()
        collection = client.get_collection("salaries")
        start_date = datetime(year, month, 1)
        end_date = start_date + relativedelta(months=1)

        pipeline = [
            {
                "$match": {
                    "user_id": user_id,
                    "date": {"$gte": start_date, "$lt": end_date}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "dollar": {"$sum": "$valute.dollar"},
                    "euro": {"$sum": "$valute.euro"},
                    "yena": {"$sum": "$valute.yena"},
                    "som": {"$sum": "$valute.som"}
                }
            },
            {
            "$project": {
                "dollar": {"$round": ["$dollar", 2]},
                "euro": {"$round": ["$euro", 2]},
                "yena": {"$round": ["$yena", 2]},
                "som": {"$round": ["$som", 2]}
                }
            }
        ]

        result = collection.aggregate(pipeline).to_list()
        if len(result) != 0:
            
            return result[0]
        return {}
    finally:
        client.close()
