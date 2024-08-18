from typing import Tuple

from sqlalchemy import select, func, update, Row
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_conf import get_async_session
from database.models import Salary


async def write_salary(
        base: int,
        overtime: int,
        earned: int,
        data_: dict
) -> None:
    """Функция для сохранения настроек пользователя."""
    session: AsyncSession = await get_async_session()
    period = 1 if int(data_["date"][:2]) <= 15 else 2

    data: dict = {
        "user_chat_id": data_["user_id"],
        "base_hours": float(base),
        "overtime": float(overtime),
        "earned": float(earned),
        "date": data_["date"],
        "period": period
    }

    salary: Salary = Salary(**data)
    session.add(salary)
    await session.commit()


async def update_salary(
        base: int,
        overtime: int,
        earned: int,
        data_: dict
) -> None:
    """Функция для обновления настроек в базе данных."""
    session: AsyncSession = await get_async_session()

    stmt = (update(Salary)
            .where(Salary.user_chat_id == data_["user_id"])
            .where(Salary.date == data_["date"])
            .values(base_hours=base, overtime=overtime, earned=earned))

    await session.execute(stmt)
    await session.commit()


async def check_record_salary(user_id: int, date: str) -> float:
    """
    Функция для проверки существуют ли у нас запись для
    данного пользователя или нет, чтобы избежать ситуации
    когда у одного пользователя может быть множество записей с одной датой.
    """
    session: AsyncSession = await get_async_session()

    stmt = (select(Salary)
            .where(Salary.user_chat_id == user_id)
            .where(Salary.date == date)
            )

    data = await session.scalars(stmt)
    await session.close()
    return data.first()


async def get_salary(
        year: str,
        month: str,
        user_id: int,
        period: int,
        session: AsyncSession
) -> Row:
    """Функция получает данные о зарплате по периодам."""
    stmt = ((
        select(
            func.sum(Salary.earned),
            func.sum(Salary.base_hours),
            func.sum(Salary.overtime)
        )
        .where(Salary.date.like(f"%/{month}/{year}"))
        .where(Salary.user_chat_id == user_id))
        .where(Salary.period == period)
        )
    data = await session.execute(stmt)
    return data.one()


async def get_total_salary(
        year: str, month: str, user_id: int
) -> Tuple[Row, Row, Row]:
    """
    Функция для получения информации о зарплате по периодам и за целый месяц.
    """
    session: AsyncSession = await get_async_session()
    period_one: Row = await get_salary(year, month, user_id, 1, session)
    period_two: Row = await get_salary(year, month, user_id, 2, session)

    stmt = ((
        select(
            func.sum(Salary.earned),
            func.sum(Salary.base_hours),
            func.sum(Salary.overtime)
        )
        .where(Salary.date.like(f"%/{month}/{year}"))
        .where(Salary.user_chat_id == user_id))
        )

    data = await session.execute(stmt)
    await session.close()
    return period_one, period_two, data.one()
