from datetime import datetime, date
from typing import Tuple

from asyncpg.pgproto.pgproto import timedelta

from database import Settings


async def get_total_price(
    first_day: int,
    days_in_month: int,
    price: Settings,
    count: int,
    hours: int
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


async def parse_data(data_: dict) -> Tuple[int, int, int, int]:
    """
    Извлекает значения месяца, года, рабочих дней и количества часов
    из переданного словаря.

    :param data_: Словарь, содержащий данные для извлечения.
                  Ожидается наличие ключей: "month", "year", "weekdays",
                  "how_many_days".

    :return: Кортеж из четырех целых чисел:
             - месяц (int)
             - год (int)
             - количество рабочих дней (int)
             - количество часов (int)
    """
    month: int = data_.get("month")
    year: int = data_.get("year")
    weekdays: int = data_.get("weekdays")
    hours: int = data_.get("how_many_hours")

    return month, year, weekdays, hours


async def get_year_and_month(action: str) -> Tuple[int, int]:
    """
    Возвращает год и месяц в зависимости от переданного действия.
    :param action: Строка, определяющая действие.
                   Если 'current', возвращает текущий год и месяц.
                   Если любое другое значение, возвращает год и месяц через
                    35 дней(чтоб наверняка) от текущей даты.

    :return: Кортеж из двух целых чисел: (год, месяц).
    """
    year, month = datetime.now().year, datetime.now().month
    if action == "next_month":
        # Получение даты через 35 дней от текущей
        next_date: date = (date(year, month, 1) + timedelta(days=35))
        # Извлечение года и месяца из следующей даты
        year, month = next_date.year, next_date.month

    return year, month
