from datetime import date, timedelta
from typing import Sequence, Tuple, List, Dict

from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from sqlalchemy import Row

from crud.statistics import get_information_for_month
from database.models import Salary
from keywords.month import create_calendar
from states.month import MonthState


async def create_message(
        user_id: int, _date: str, state: FSMContext
) -> InlineKeyboardMarkup:
    """
    Функция собирает информацию для отображения календаря и сообщения о зарплате.
    :param user_id: ID пользователя.
    :param _date: Переданная дата
    :param state: Состояние.
    :return: Сообщение и календарь.
    """
    year: int = int(_date[:4])
    month: int = int(_date[5:7])
    await state.clear()
    await state.set_state(MonthState.choice)

    result: Sequence[Row[tuple[Salary]]] = \
        await get_information_for_month(user_id, year, month)
    await state.update_data(year=year, month=month, result=result)

    return await create_calendar(result, year, month)


async def generate_str(iterable: Sequence[Row[tuple[Salary]]]) -> str:
    """
    Генерация сообщения с подробной информацией за месяц
    об отработанных часах и заработанной сумме.

    :param iterable: Объект запроса к бд.
    :return: Строку для показа пользователю.
    """
    one: List[int] = [0, 0, 0]
    two: List[int] = [0, 0, 0]
    total: List[int] = [0, 0, 0]

    if iterable is None:
        raise KeyError

    for sal in iterable:
        total[0] += sal[0].base_hours + sal[0].overtime
        total[1] += sal[0].overtime
        total[2] += sal[0].earned + (sal[0].other_income
                                     if sal[0].other_income else 0)

        if sal[0].period == 1:
            one[0] += sal[0].base_hours + sal[0].overtime
            one[1] += sal[0].overtime
            one[2] += sal[0].earned + (sal[0].other_income
                                       if sal[0].other_income else 0)

        if sal[0].period == 2:
            two[0] += sal[0].base_hours + sal[0].overtime
            two[1] += sal[0].overtime
            two[2] += sal[0].earned + (sal[0].other_income
                                       if sal[0].other_income else 0)
    northern: float = total[0] * 25
    northern_1: float = one[0] * 25
    northern_2: float = two[0] * 25
    string: str = (f"П1: {one[0]}ч | {one[1]}ч | {one[2] - northern_1:,.1f}₽ | {northern_1}₽ \n"
                   f"П2: {two[0]}ч | {two[1]}ч | {two[2] - northern_2:,.1f}₽ | {northern_2}₽ \n"
                   f"Месяц: {total[0]}ч | {total[1]}ч | {total[2]:,.1f}₽ \n"
                   f"Без северных: {total[2] - northern}₽\n"
                   f"Северные: {northern}₽")
    return string


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
