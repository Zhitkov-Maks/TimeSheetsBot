from calendar import monthrange
from datetime import datetime, date
from typing import Tuple

from asyncpg.pgproto.pgproto import timedelta
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import Settings
from database.db_conf import get_async_session
from utils.count import Employee


async def get_total_price(
    first_day: int,
    days_in_month: int,
    price: Settings,
    count: int,
    hours
) -> int:
    """
    Функция для подсчета суммы зарплаты 2/2 за месяц.
    :param first_day: Первая смена в месяце.
    :param days_in_month: Количество дней в месяце.
    :param price: Настройки стоимости за час.
    :param count: Количество доп смен в месяц.
    :param hours: По сколько часов считается смена.
    :return: Прогнозируемую сумму.
    """
    total_sum: int = 0
    for i in range(first_day, days_in_month + 1, 4):
        total_sum += hours * price.price

        if i + 1 <= days_in_month:
            total_sum += hours * price.price

    total_sum += ((price.price + price.overtime) * hours) * count
    return total_sum



async def two_in_two_get_prediction_sum(user_id: int, data_: dict) -> tuple:
    """
    Функция для вычисления ожидаемой зп.
    :param user_id: Id юзера.
    :param data_: Дополнительные данные.
    :return: Прогнозируемую сумму.
    """
    year: int = data_.get("year")
    month: int = data_.get("month")
    hours: int = data_.get("how_many_hours")
    # Получим настройки стоимости для конкретного пользователя
    session: AsyncSession = await get_async_session()

    stmt: Select = select(Settings).where(Settings.user_chat_id == user_id)
    price: Settings | None = await session.scalar(stmt)

    if price is None:
        price: Employee = Employee(300, 100)

    # Получаем количество дней в месяце.
    days_in_month: int = monthrange(year, month)[1]

    # Первая смена в месяце.
    first_day: int = data_.get("first_day")

    # Количество дней с подработками.
    count_weekdays: int = data_.get("weekdays")

    await session.close()

    # Если первая смена второго, то проблем нет и просто считаем сумму.
    if first_day > 1:
        total_sum: int = await get_total_price(
            first_day, days_in_month, price, count_weekdays, hours)
        return total_sum,


    else:
        # Первый вариант если смены 1 и второго
        total_sum: int = await get_total_price(
            first_day, days_in_month, price, count_weekdays, hours)

        # Второй вариант, если смена 1 а 2 выходной
        total_sum_two: int = await get_total_price(
            first_day + 3, days_in_month, price, count_weekdays, hours
        )
        sum_by_day = price.price * hours
        return total_sum, total_sum_two + sum_by_day



async def get_prediction_sum(user_id: int, data_: dict) -> int:
    """
    Функция для вычисления ожидаемой зп. Подсчет основан на том основании,
    что у меня один доп и 2 раза в неделю остаюсь до семи.
    :param user_id: Id юзера.
    :param data_: Id юзера.
    :return: Прогнозируемую сумму.
    """
    # Получаем необходимые переменные для подсчета.
    month, year, weekdays, hours = await parse_data(data_)
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
        delay: str | list = data_.get("delay")
        hour: int = int(data_.get("hour"))

        if delay == "delay_no":
            if wd in (range(5)):
                total_sum += price.price * hours

        else:
            if wd in delay:
                total_sum += price.price * hours + (
                            price.price + price.overtime) * hour
            elif wd in (range(5)):
                total_sum += price.price * hours

    total_sum += ((price.price + price.overtime) * hours) * weekdays
    await session.close()
    return total_sum


async def parse_data(data_: dict) -> Tuple[int, int, int, int]:
    month: int = data_.get("month")
    year: int = data_.get("year")
    weekdays: int = data_.get("weekdays")
    hours: int = data_.get("how_many_days")
    return month, year, weekdays, hours


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
