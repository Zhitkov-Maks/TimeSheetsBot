from datetime import date, timedelta
from typing import Tuple, Dict

from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup

from keyboards.month import create_calendar
from states.month import MonthState
from crud.statistics import get_information_for_month
from crud.create import aggregate_data
from crud.settings import get_settings_user_by_id

from loader import money


async def get_number_hours(user_id: int) -> float:
    """
    Функция возвращает настройки, для показа
    суммы доплаты за переработку.
    """
    settings = await get_settings_user_by_id(user_id)
    return (
        float(settings.get("data").get("number_hours_per_month")),
        float(settings.get("data").get("price_overtime"))
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


async def generate_str(year: int, month: int, user_id: int) -> str:
    """
    Генерация сообщения с подробной информацией за месяц
    об отработанных часах и заработанной сумме.

    :param iterable: Объект запроса к бд.
    :return: Строку для показа пользователю.
    """
    hours_min, overtime = await get_number_hours(user_id)
    message: str = f"Данные за {month}/{year}\n\n"
    period_one: dict = await aggregate_data(year, month, user_id, period=1)
    period_two: dict = await aggregate_data(year, month, user_id, period=2)

    total_hours = period_one.get("total_base_hours", 0) + \
        period_two.get("total_base_hours", 0)

    if total_hours > hours_min:
        overtime *= (total_hours - hours_min)
    else:
        overtime = 0

    total_earned = period_one.get("total_earned", 0) + \
        period_two.get("total_earned", 0)

    total_cold = period_one.get("total_earned_cold", 0) + \
        period_two.get("total_earned_cold", 0)

    message += f"Период с 1-15: \nOтработано часов - {
            period_one.get("total_base_hours", 0)
        }ч\n" + f"Заработано денег - {
                period_one.get("total_earned", 0)}{money}\n\n"

    message += f"Период с 16-31: \nOтработано часов - {
        period_two.get("total_base_hours", 0)
        }ч\n" + f"Заработано денег - {
            period_two.get("total_earned", 0)}{money}\n\n"

    message += f"За весь месяц: \nOтработано часов - {total_hours}ч\n" \
               f"Заработано денег - {total_earned}{money}\n" \
               f"Северные за месяц - {total_cold}{money}\n" \
               f"Доплата за переработку часов - {overtime}{money}\n\n"

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
    else:
        find_date: date = parse_date + timedelta(days=30)

    return find_date.year, find_date.month
