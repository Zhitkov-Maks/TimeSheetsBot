from datetime import datetime, UTC

import pymongo

from database.db_conf import MongoDB
from utils.calculate import calc_valute


async def write_other(data: dict, user: int) -> bool:
    """
    Add a new income record (without updating the existing ones).

    :param data: Recording data.
    :param user: ID user.
    :return: True on success, False on error.
    """
    type_operation: str = data.get("type_")
    required = {"amount", "description", "month", "year"}
    if not all(field in data for field in required):
        return False

    client = MongoDB()
    try:
        if type_operation == "income":
            collection = client.get_collection("other_income")
        else:
            collection = client.get_collection("expences")

        record = {
            "user_id": user,
            "amount": float(data["amount"]),
            "description": data["description"],
            "month": int(data["month"]),
            "year": int(data["year"]),
            "created_at": datetime.now(UTC)
        }

        result = collection.insert_one(record)
        return result.acknowledged

    except Exception:
        return False
    finally:
        client.close()


async def write_salary(
    data: dict,
    user_id: int,
    date: datetime,
    valute_data: dict[str, tuple[int, float]]
) -> None:
    """
    Save or update the user's settings.

    :param base: The base rate.
    :param earned_hours: Earned in hours.
    :param earned_cold: Additional payment for the cold.
    :param data_: Dictionary with data to record.
    :param valute_data: Information about the ruble exchange rate.
    """
    client: MongoDB = MongoDB()
    period: int = 1 if date.day <= 15 else 2
    earned_in_valute = await calc_valute(data.get("earned"), valute_data)
    data.update(
        period=period,
        valute=earned_in_valute,
        date_write=datetime.now(UTC)
    )
    collection = client.get_collection("salaries")

    collection.create_index(
        [("user_id", 1), ("date", 1)],
        unique=True,
        name="unique_user_date"
    )
    
    try:
        collection.update_one(
            {"user_id": user_id, "date": date},
            {"$set": data},
            upsert=True
        )
    except pymongo.errors.DuplicateKeyError:
        pass
    finally:
        client.close()


async def delete_record(date: str, user_id) -> None:
    """
    Deleted the records from the database by user ID and date.

    :param date: The date of the record being deleted.
    :param user_id: The user's ID.
    """
    try:
        client: MongoDB = MongoDB()
        parse_date = datetime.strptime(date, "%Y-%m-%d")
        collection = client.get_collection("salaries")
        collection.delete_one({
            "user_id": user_id,
            "date": parse_date
        })
        client.close()
    finally:
        client.close()


async def remove_other_income_expese(collections: str, id_: str) -> None:
    """
    Delete the records from the database by record ID.

    :param collections: Type of collection (other income or expenses).
    :param id_: The ID of the record.
    """
    try:
        client: MongoDB = MongoDB()
        collection = client.get_collection(collections)
        collection.delete_one({
            "_id": id_
        })
    finally:
        client.close()
