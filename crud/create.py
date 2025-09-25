from datetime import datetime, UTC

import pymongo

from database.db_conf import MongoDB


async def write_other(data: dict, user: int) -> bool:
    """
    Добавляет новую запись о доходе (без обновления существующих).

    :param data: Данные для записи
    :param user: ID пользователя
    :return: True при успехе, False при ошибке
    """
    type_operation = data.get("type_")
    required = {"amount", "description", "month", "year"}
    if not all(field in data for field in required):
        return False

    client = MongoDB()
    try:
        if type_operation == "income":
            collection = client.get_collection("other_income")
        else:
            collection = client.get_collection("expences")

        # Генерируем уникальный ID для каждой записи
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
        base: float, earned_hours, earned_cold: float, data_: dict
) -> None:
    """
    Функция для сохранения и обновления настроек пользователя.

    :param data_settings: Словарь с данными для записи.
    """
    client: MongoDB = MongoDB()
    period: int = 1 if int(data_["date"][-2:]) <= 15 else 2
    parse_date = datetime.strptime(data_["date"], "%Y-%m-%d")
    user_id = data_["user_id"]
    earned = earned_hours + earned_cold

    data: dict = {
        "base_hours": float(base),
        "earned": float(earned),
        "earned_hours": earned_hours,
        "earned_cold": earned_cold,
        "period": period,
    }

    collection = client.get_collection("salaries")

    # Создаем уникальный индекс (если его еще нет)
    collection.create_index(
        [("user_id", 1), ("date", 1)],
        unique=True,
        name="unique_user_date"
    )
    
    try:
        collection.update_one(
            {"user_id": user_id, "date": parse_date},
            {"$set": data},
            upsert=True
        )
    except pymongo.errors.DuplicateKeyError:
        pass
    finally:
        client.close()


async def delete_record(date: str, user_id) -> None:
    """
    Удаление записи из бд по ID пользователя и дате.

    :param date: Дата удаляемой записи.
    :param user_id: Идентификатор пользователя.
    """
    client: MongoDB = MongoDB()
    parse_date = datetime.strptime(date, "%Y-%m-%d")
    collection = client.get_collection("salaries")
    collection.delete_one({
        "user_id": user_id,
        "date": parse_date
    })
    client.close()
