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
