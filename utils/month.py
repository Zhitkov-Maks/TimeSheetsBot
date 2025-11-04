from datetime import date, timedelta
from typing import Tuple, Dict
import asyncio

from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup

from keyboards.month import create_calendar
from states.month import MonthState
from crud.statistics import (
    get_information_for_month,
    aggregate_data,
    get_other_sum
)
from crud.settings import get_settings_user_by_id

from loader import money, MONTH_DATA


async def get_settings(user_id: int) -> float:
    """
    Return the user's settings.
    
    :param user_id: The user's ID.
    """
    settings: dict = await get_settings_user_by_id(user_id)
    return (
        float(settings.get("price_overtime", 0)),
        float(settings.get("price_cold", 0))
    )


async def create_message(
        user_id: int, _date: str, state: FSMContext
) -> InlineKeyboardMarkup:
    """
    Collect the information to display in the calendar.

    :param user_id: The user's ID.
    :param _date: The transmitted date.
    :param state: Condition.
    :return: Message and calendar.
    """
    year: int = int(_date[:4])
    month: int = int(_date[5:7])
    await state.clear()
    await state.set_state(MonthState.choice)

    result = await get_information_for_month(user_id, year, month)
    await state.update_data(year=year, month=month, result=result)

    return await create_calendar(result, year, month)


async def create_message_for_period(data: tuple, period: str) -> str:
    """
    Create a line about the information for the period.
    
    :param data: A tuple with information for the period.
    :param perion: A string for displaying the period.
    :return str: A message to the user.
    """
    money_: str = ""
    if data[4]:
        money_ += (
            f"Доплата за холод: {data[4]:,}{money}.\n"
        )
    if data[3] is not None:
        money_ += (
            f"Премия: {data[2]:,}{money}({data[3]})\n"
        )

    return (
        f"\nПериод с {period}:\n"
        f"----------------------------------------\n"
        f"Отработано часов: {data[1]}ч.\n"
        f"Итого заработано: {data[0]:,}{money}.\n"
        f"Из них оплата часов: {data[5]:,}{money}.\n"
        f"{money_}\n"
    )


async def get_data_from_db(year: int, month: int, user_id: int) -> tuple:
    """
    Get the calculation data from the database.
    
    :param year: The year for the request.
    :param month: The month for the request.
    :param user_id: The user's ID.
    :return tuple: A tuple with data.
    """
    return (
        await asyncio.gather(
            aggregate_data(year, month, user_id, period=1),
            aggregate_data(year, month, user_id, period=2),
            get_other_sum(year, month, user_id, "income"),
            get_other_sum(year, month, user_id, "expence"),
            return_exceptions=False
        )
    )
    

async def calculation_by_part(data: dict) -> tuple[float]:
    """
    Return the tuple with the necessary data.
    
    :param data: A dictionary with input data.
    :return list: A list with calculation data.
    """
    earned: float = data.get("total_earned", 0)
    hours: float = data.get("total_base_hours", 0)
    earned_hours: float = data.get("total_earned_hours")
    award: float = data.get("total_award", 0)
    count_operations: float = data.get("total_operations", 0)
    earned_cold: float = data.get("total_earned_cold", 0)
    return (
        earned,
        hours,
        award,
        count_operations,
        earned_cold,
        earned_hours
    )

    
async def data_calculation(
    data: tuple
) -> list[tuple | float]:
    """
    Collect the data for further work with them.
    
    :param data: A tuple with data.
    :return list: A list with data.
    """
    period_1: tuple = await calculation_by_part(data[0])
    period_2: tuple = await calculation_by_part(data[1])
    
    hours: float = period_1[1] + period_2[1]
    income: float = data[2].get("total_sum", 0)
    expense: float = data[3].get("total_sum", 0)
    award: float = period_1[2] + period_2[2]
    operations: float = period_1[3] + period_2[3]
    total_earned: float = (
        period_1[0] + period_2[0] + award + income - expense
    )
    return [
        period_1,
        period_2,
        income,
        expense,
        award,
        operations,
        total_earned,
        hours
    ]


async def generate_str(year: int, month: int, user_id: int) -> str:
    """
    Generate a message with detailed information for the month.

    :param year: A year to collect information.
    :param month: A month to collect information.
    :param user_id: User ID.
    :return: A line to show to the user.
    """
    overtime, _ = await get_settings(user_id)
    message: str = f"Данные за {month}/{year}\n\n"
    total_data: tuple = await get_data_from_db(year, month, user_id)
    data: list = await data_calculation(total_data)

    hours_ = 190 if month != 2 else 180  # Норма часов в месяц.

    award_message = (
            f"Премия: {data[4]}{money}({data[5]})\n"
            if data[4] is not None else ''
        )

    pay_overtime_str = ""

    if data[7] > hours_:
        data[6] += overtime * (data[7] - hours_)
        pay_overtime_str = "Доплата за переработку: " + \
            f"{overtime * (data[7] - hours_):,}{money}\n"

    message += await create_message_for_period(data[0], "1-15")
    message += await create_message_for_period(data[1], "16-го")

    message += (
        f"\nЗа {MONTH_DATA[month]} {year}:\n"
        f"----------------------------------------\n"
        f"Отработано часов: {data[7]:,}ч.\n"
        f"Заработано денег: {data[6]:,}{money}.\n"
    )

    message += pay_overtime_str
    message += award_message
    message += (f"Прочие доходы: {data[2]:,}{money}\n")
    message += (f"Списание под зп: {data[3]:,}{money}\n")
    return message


async def get_date(data: Dict[str, str], action: str) -> Tuple[int, int]:
    """
    Return the required month (next or previous).

    :param data: Dictionary with year and month
    :param action: The selected action is prev or next.
    :return: Year and month.
    """
    parse_date: date = date(int(data["year"]), int(data["month"]), 5)

    if action == "prev":
        find_date: date = parse_date - timedelta(days=30)

    elif action == "next":
        find_date: date = parse_date + timedelta(days=30)

    else:
        find_date = parse_date
    return find_date.year, find_date.month
