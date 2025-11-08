from datetime import datetime
from dateutil.relativedelta import relativedelta

from database.db_conf import MongoDB

import pymongo


async def get_salary_for_day(day_id: str) -> None:
    """
    Get the data for the day.

    :param daн_id: The ID of the record.
    """
    try:
        client = MongoDB()
        collection = client.get_collection("salaries")
        data: dict = collection.find_one({"_id": day_id})
        return data
    finally:
        client.close()
        
        
async def get_hours_for_month(
    user_id: int,
    year: int, 
    month: int
) -> dict:
    """
    Aggregate the hours for the month.

    :param user_id: The user's ID.
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
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_hours": {"$sum": "$base_hours"}
                }
            },
            {
                "$project": {
                    "total_hours": {"$round": ["$total_hours", 1]}
                }
            }
        ]

        result = collection.aggregate(pipeline).to_list()
        if result and len(result) > 0:
            return result[0].get("total_hours", 0.0)
        return 0.0
    finally:
        client.close()


async def update_salary(
    day_id: int, data: dict
) -> None:
    """
    Update your salary for the day.

    :param day_id: ID of the day.
    :param data: Dictionary with data to record.
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
