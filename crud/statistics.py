from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, asc, Sequence, Select, func, extract, Row, Result
from database.db_conf import get_async_session
from database.models import Salary


async def request_statistic(user: int, year: int) -> Row[tuple]:
    """
    Запрос на получение небольшой статистики за год.
    :param user: Id юзера.
    :param year: Год для статистики.
    :return: Кортеж со статистикой.
    """
    session: AsyncSession = await get_async_session()
    # Запрос для получения итогового заработка за год
    stmt: Select = (
        select(
            func.sum(Salary.earned),
            func.sum(Salary.base_hours),
            func.sum(Salary.overtime),
        )
        .where(Salary.user_chat_id == user)
        .where(
            (extract("year", func.date(Salary.date)) == year),
        )
    )
    data: Result = await session.execute(stmt)
    await session.close()
    return data.one()


async def get_information_for_month(user_id: int, year: int, month: int) -> Sequence:
    """
    Получение данных за выбранный месяц.
    :param user_id: Id юзера.
    :param year: Год.
    :param month: Месяц.
    :return: Возвращает данные за месяц, чтобы сформировать календарь.
    """
    session: AsyncSession = await get_async_session()
    month: str = str(month) if month > 9 else f"0{month}"

    stmt: Select = (
        select(Salary)
        .where(Salary.user_chat_id == user_id)
        .where(func.extract("year", Salary.date) == int(year))  # Фильтрация по году
        .where(func.extract("month", Salary.date) == int(month))
        .order_by(asc(Salary.date))
    )

    data: Result = await session.execute(stmt)
    await session.close()
    return data.all()


async def get_info_by_date(user_id: int, date: str) -> Salary:
    """
    Показ данных за выбранное число.
    :param user_id: Идентификатор пользователя.
    :param date: Выбранная дата.
    :return: Данные за выбранный месяц.
    """
    session: AsyncSession = await get_async_session()
    parse_date: date = datetime.strptime(date, "%Y-%m-%d")
    stmt: Select = (
        select(Salary)
        .where(Salary.user_chat_id == user_id)
        .where(Salary.date == parse_date)
    )
    data: Salary = await session.scalar(stmt)
    await session.close()
    return data
