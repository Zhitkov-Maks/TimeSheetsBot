from calendar import monthrange
from datetime import datetime, date
from typing import Tuple

from asyncpg.pgproto.pgproto import timedelta
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import Settings
from database.db_conf import get_async_session
from utils.count import Employee


async def two_in_two_get_prediction_sum(user_id: int, data_: dict) -> int:
    """
    Функция для вычисления ожидаемой зп.
    :param user_id: Id юзера.
    :param data_: Дополнительные данные.
    :return: Прогнозируемую сумму.
    """
    year: int = data_.get("year")
    month: int = data_.get("month")
    # Получим настройки стоимости для конкретного пользователя
    session: AsyncSession = await get_async_session()

    stmt: Select = select(Settings).where(Settings.user_chat_id == user_id)
    price: Settings | None = await session.scalar(stmt)

    if price is None:
        price: Employee = Employee(300, 100)

    # Получаем количество дней в месяце.
    days_in_month: int = monthrange(year, month)[1]

    first_day: int = data_.get("first_day")
    weekdays: int = data_.get("weekdays")

    total_sum: int = 0
    for i in range(first_day, days_in_month + 1, 4):
        total_sum += 12 * price.price

        if i + 1 <= days_in_month:
            total_sum += 12 * price.price

    total_sum += ((price.price + price.overtime) * 12) * weekdays
    await session.close()
    return total_sum


async def get_prediction_sum(user_id: int, data_: dict) -> int:
    """
    Функция для вычисления ожидаемой зп. Подсчет основан на том основании,
    что у меня один доп и 2 раза в неделю остаюсь до семи.
    :param user_id: Id юзера.
    :param data_: Id юзера.
    :return: Прогнозируемую сумму.
    """
    # Получим настройки стоимости для конкретного пользователя
    month, year, weekdays = await parse_data(data_)
    session: AsyncSession = await get_async_session()

    stmt: Select = select(Settings).where(Settings.user_chat_id == user_id)
    price: Settings | None = await session.scalar(stmt)

    if price is None:
        price: Employee = Employee(300, 100)

    # Получаем количество дней в месяце.
    days_in_month: int = monthrange(year, int(month))[1]
    month: str = str(month) if int(month) > 9 else f"0{month}"

    total_sum: int = 0
    for i in range(1, days_in_month + 1):
        days: str = str(i) if i > 9 else f"0{i}"
        wd = datetime.strptime(f"{days}-{month}-{year}", "%d-%m-%Y").weekday()

        if data_.get("delay") == "delay_no":
            if wd in (range(5)):
                total_sum += price.price * 9
        else:
            count, hours = await parse_delay(data_.get("delay"))
            if count < 3:
                if wd in (1, 3):
                    total_sum += price.price * 9 + (price.price + price.overtime) * hours
                elif wd in (0, 2, 4):
                    total_sum += price.price * 9

            else:
                if wd in (0, 1, 2):
                    total_sum += price.price * 9 + (price.price + price.overtime) * hours
                elif wd in (3, 4):
                    total_sum += price.price * 9


    total_sum += ((price.price + price.overtime) * 9) * weekdays
    await session.close()
    return total_sum


async def parse_data(data_: dict) -> Tuple[int, int, int]:
    month: int = data_.get("month")
    year: int = data_.get("year")
    weekdays: int = data_.get("weekdays")
    return month, year, weekdays


async def parse_delay(overtime_data: str) -> tuple:
    count_overtime, hours_overtime = overtime_data.split("/")
    return int(count_overtime), int(hours_overtime)


async def get_year_and_month(action: str) -> Tuple[int, int]:
    """
    Функция возвращает либо текущий, либо следующий месяц.
    """
    if action == "current":
        year, month = datetime.now().year, datetime.now().month
    else:
        next_date: date = (datetime.now() + timedelta(days=30)).date()
        year, month = next_date.year, next_date.month
    return year, month
