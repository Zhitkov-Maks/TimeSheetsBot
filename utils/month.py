from datetime import date, timedelta, datetime, UTC
from typing import Tuple, Dict

from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup

from keyboards.month import create_calendar
from states.month import MonthState
from crud.statistics import get_information_for_month
from loader import money, MONTH_DATA
from utils.calculate import data_calculation, generate_data
from utils.settings import get_settings
from utils.statistic import get_data_from_db


async def get_message_for_period(data: tuple, name: str) -> str:
    """
    Create a message to send to the user.
    
    :param data: A tuple with the necessary data.
    :param name: The name of the command.
    """
    number = f"{name[-1]} период" if name[-1].isdigit() else "месяц"
    message = f"Инфо за {number}.\n"
    message += (
        f"Итого: {data[0]:,}{money}.\n"
        f"Часов: {data[1]}ч.\n"
        f"Часы: {(data[5]):,}{money}.\n"
    )

    if data[3]:
        message += f"Премия: {data[2]:,}{money}({data[3]}).\n"

    if data[4]:
        message += f"Холод: {data[4]:,}{money}.\n"

    if data[6]:
        message += f"Переработка: {data[6]}{money}.\n"
        message += f"Часов пе-ки: {data[7]}ч.\n"

    return message


async def get_amount_and_hours_for_month(
    year: int,
    month: int,
    user_id: int,
    state: FSMContext
) -> tuple[tuple]:
    """
    Return the most necessary data for display.
    
    :param year: A year to collect information.
    :param month: A month to collect information.
    :param user_id: User ID.
    """
    total_data: tuple = await get_data_from_db(year, month, user_id)
    data: list = await data_calculation(total_data)

    period1: tuple[float] = (data[0][0], data[0][1])
    period2: tuple[float] = (data[1][0], data[1][1])

    await state.update_data(
        period1=data[0],
        period2=data[1],
        for_month=await generate_data(data, data[0], data[1])
    )

    return period1, period2, (data[6], data[7])


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
    
    data: tuple[tuple] = (
        await get_amount_and_hours_for_month(
            year, month, user_id, state
        )
    )

    result = await get_information_for_month(user_id, year, month)
    await state.update_data(year=year, month=month, result=result)

    return await create_calendar(result, year, month, data)


async def generate_str(year: int, month: int, user_id: int) -> str:
    """
    Generate a message with detailed information for the month.

    :param year: A year to collect information.
    :param month: A month to collect information.
    :param user_id: User ID.
    :return: A line to show to the user.
    """
    total_data: tuple = await get_data_from_db(year, month, user_id)
    data: list = await data_calculation(total_data)

    hours_ = 190 if month != 2 else 180  # Норма часов в месяц.

    award_message = (
            f"Премия: {data[4]}{money}({data[5]}).\n"
            if data[5] else ''
        )

    pay_overtime_str = ""

    if data[7] > hours_:
        overtime = data[0][6] + data[1][6]
        pay_overtime_str = (
                f"Переработка: {overtime:,}{money}.\n"
                f"Часов пере-ки: {data[0][7] + data[1][7]}ч.\n"
            )

    message = (
        f"\n{MONTH_DATA[month]} {year}:\n"
        f"----------------------------------------\n"
        f"Отработано часов: {data[7]:,}ч.\n"
    )
    
    if data[8] > 0:
        message += f"Доплата за холод: {data[8]:,}{money}\n"
    

    message += pay_overtime_str
    message += award_message
    message += (
        f"Прочие доходы: {data[2]:,}{money}.\n" if data[2] else ""
    )
    message += (
        f"Списание под зп: {data[3]:,}{money}.\n" if data[3] else ""
    )
    
    message += (
        f"----------------------------------------\n"
        f"Итого: {data[6]:,}{money}\n"
        f"----------------------------------------\n"
    )

    return message


async def get_date(data: Dict[str, str], action: str) -> Tuple[int, int]:
    """
    Return the required month (next or previous).

    :param data: Dictionary with year and month
    :param action: The selected action is prev or next.
    :return: Year and month.
    """
    year, month = data.get("year"), data.get("month")
    if year is None and month is None:
        current_date = datetime.now(UTC)
        return current_date.year, current_date.month
    
    parse_date: date = date(int(year), int(month), 5)
    if action == "prev":
        find_date: date = parse_date - timedelta(days=30)

    elif action == "next":
        find_date: date = parse_date + timedelta(days=30)

    else:
        find_date = parse_date
    return find_date.year, find_date.month
