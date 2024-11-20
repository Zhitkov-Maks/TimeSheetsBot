from datetime import datetime, date
from typing import Dict

from sqlalchemy import update, delete, Delete, Update
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_conf import get_async_session
from database.models import Salary


async def write_salary(
    base: float, overtime: float, earned: float, data_: Dict[str, int | str]
) -> None:
    """
    Функция для сохранения записи о смене.
    :param base: Базовая ставка
    :param overtime: Доплата за переработку.
    :param earned: Итого заработано.
    :param data_: Словарь с остальными данными.
    """
    session: AsyncSession = await get_async_session()
    period: int = 1 if int(data_["date"][-2:]) <= 15 else 2
    parse_date: date = datetime.strptime(data_["date"], "%Y-%m-%d")

    data: dict = {
        "user_chat_id": data_["user_id"],
        "base_hours": float(base),
        "overtime": float(overtime),
        "earned": float(earned),
        "date": parse_date,
        "period": period,
    }

    salary: Salary = Salary(**data)
    session.add(salary)
    await session.commit()


async def update_salary(
    base: float, overtime: float, earned: float, data_: Dict[str, int | str]
) -> None:
    """
    Функция для обновления данных о смене в базе данных.
    :param base: Базовая ставка.
    :param overtime: Доплата за переработку.
    :param earned: Итого заработано.
    :param data_: Словарь с остальными данными.
    """
    session: AsyncSession = await get_async_session()
    parse_date: date = datetime.strptime(data_["date"], "%Y-%m-%d")

    stmt: Update = (
        update(Salary)
        .where(Salary.user_chat_id == data_["user_id"])
        .where(Salary.date == parse_date)
        .values(base_hours=base, overtime=overtime, earned=earned)
    )

    await session.execute(stmt)
    await session.commit()


async def delete_record(data: Dict[str, str | int]) -> None:
    """
    Функция для удаления записи за выбранное число.
    :param data:
    :return:
    """
    session: AsyncSession = await get_async_session()
    parse_date: date = datetime.strptime(data["date"], "%Y-%m-%d")
    stmt: Delete = (
        delete(Salary)
        .where(Salary.user_chat_id == data["user_id"])
        .where(Salary.date == parse_date)
    )
    await session.execute(stmt)
    await session.commit()
    await session.close()
