from datetime import date, timedelta
from typing import Tuple, Dict

from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup

from keyboards.month import create_calendar
from states.month import MonthState
from crud.statistics import get_information_for_month, aggregate_data
from crud.settings import get_settings_user_by_id

from loader import money, MONTH_DATA


async def get_settings(user_id: int) -> float:
    """
    Функция возвращает настройки, для показа
    суммы доплаты за переработку.
    """
    settings = await get_settings_user_by_id(user_id)
    return (
        float(settings.get("price_overtime", 0)),
        float(settings.get("price_cold", 0))
    )


async def create_message(
        user_id: int, _date: str, state: FSMContext
) -> InlineKeyboardMarkup:
    """
    Функция собирает информацию для отображения календаря и
    сообщения о зарплате.

    :param user_id: ID пользователя.
    :param _date: Переданная дата
    :param state: Состояние.
    :return: Сообщение и календарь.
    """
    year: int = int(_date[:4])
    month: int = int(_date[5:7])
    await state.clear()
    await state.set_state(MonthState.choice)

    result = await get_information_for_month(user_id, year, month)
    await state.update_data(year=year, month=month, result=result)

    return await create_calendar(result, year, month)


async def create_message_for_period(
        hours: float, earned: float, period: str, cold
    ) -> str:

    money_cold = ""
    if cold:
        money_cold += f"""Из них оплата часов: {earned - (hours * cold)}{money}
    Доплата за холод: {hours * cold}{money}"""
        
    return f"""
    Период с {period}:
    ----------------------------------------
    Отработано часов: {hours}ч.
    Итого заработано: {earned}{money}.
    {money_cold}
    """


async def generate_str(year: int, month: int, user_id: int) -> str:
    """
    Генерация сообщения с подробной информацией за месяц
    об отработанных часах и заработанной сумме.

    :param iterable: Объект запроса к бд.
    :return: Строку для показа пользователю.
    """
    overtime, cold = await get_settings(user_id)
    message: str = f"Данные за {month}/{year}\n\n"

    period_one: dict = await aggregate_data(year, month, user_id, period=1)
    period_two: dict = await aggregate_data(year, month, user_id, period=2)
    hours = 190 if month != 2 else 180 # Норма часов в месяц.

    hours_1 = period_one.get("total_base_hours", 0)
    hours_2 = period_two.get("total_base_hours", 0)

    total_hours =  hours_1 + hours_2

    pay_overtime_str = ""
    if total_hours > hours:
        pay_overtime_str = f"Доплата за переработку - {
            overtime * (total_hours - hours)}{money}\n"

    total_earned = period_one.get("total_earned", 0) + \
        period_two.get("total_earned", 0)
    
    message += await create_message_for_period(
        hours_1, period_one.get("total_earned", 0), "1-15", cold
    )

    message += await create_message_for_period(
        hours_2, period_two.get("total_earned", 0), "16-го", cold
    )

    message += f"""
    За {MONTH_DATA[month]} {year}:
    ----------------------------------------
    Отработано часов: {total_hours}ч.
    Заработано денег: {total_earned}{money}.
    """
    message += pay_overtime_str
    return message


async def get_date(data: Dict[str, str], action: str) -> Tuple[int, int]:
    """
    Функция получает текущую переданную дату, и в зависимости от выбранного
    действия либо прибавляет, либо убавляет месяц.

    :param data: Словарь с годом и месяцем
    :param action: Выбранное действие prev or next.
    :return: Год и месяц
    """
    parse_date: date = date(int(data["year"]), int(data["month"]), 5)

    if action == "prev":
        find_date: date = parse_date - timedelta(days=30)

    elif action == "next":
        find_date: date = parse_date + timedelta(days=30)
        
    else:
        find_date = parse_date
    return find_date.year, find_date.month
