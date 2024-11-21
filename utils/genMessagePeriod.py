from calendar import monthrange
from datetime import date
from typing import List, Dict, Tuple

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import hbold
from asyncpg.pgproto.pgproto import timedelta
from sqlalchemy import Sequence

from database.models import Salary
from keywords.keyword import month_tuple

# Для добавления в календарь.
days_list: tuple = ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")

# Добавляем в календарь символы unicode чтобы
# календарь выглядел более менее прилично.
UNICODE_DATA: Dict[int, str] = {
    1: "₁",
    2: "₂",
    3: "₃",
    4: "₄",
    5: "₅",
    6: "₆",
    7: "₇",
    8: "₈",
    9: "₉",
    10: "₁₀",
    11: "₁₁",
    12: "₁₂",
    13: "₁₃",
    14: "₁₄",
    15: "₁₅",
    16: "₁₆",
    17: "₁₇",
    18: "₁₈",
    19: "₁₉",
    20: "₂₀",
    21: "₂₁",
    22: "₂₂",
    23: "₂₃",
    24: "₂₄",
}


async def create_calendar(
    salary: Sequence, year: int, month: int
) -> InlineKeyboardMarkup:
    """
    Функция генерирует календарь за месяц который был передан в параметрах.
    :param salary: Результат запроса в бд за переданный месяц.
    :param year: Переданный год.
    :param month: Переданный месяц
    :return: Инлайн клавиатуру.
    """
    field_size: int = 5
    days: int = 35

    dates: Dict[str, int] = {
        str(sal[0].date): int(sal[0].base_hours + sal[0].overtime) for sal in salary
    }
    day_week: int = date(year, month, 1).weekday()
    days_in_month: int = monthrange(year, month)[1]

    month_keyword: List[List[InlineKeyboardButton]] = []
    if day_week + days_in_month > 35:
        field_size = 6
        days = 42

    elif days_in_month + day_week < 29:
        field_size = 4
        days = 28

    numbers_list: List[str] = (
        [" "] * day_week
        + [f"{i:02}" for i in range(1, days_in_month + 1)]
        + [" "] * (days - days_in_month - day_week)
    )

    for i in range(7):
        row: List[InlineKeyboardButton] = [
            InlineKeyboardButton(text=days_list[i], callback_data=days_list[i])
        ]
        day = i

        for _ in range(field_size):
            create_date: str = f"{year}-{month:02}-{numbers_list[day]}"
            if numbers_list[day] == " ":
                text = " "

            elif create_date in dates:
                text = f"{numbers_list[day]} {UNICODE_DATA[dates[create_date]]}"
            else:
                text = f"{numbers_list[day]}"

            row.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=create_date,
                )
            )
            day += 7
        month_keyword.append(row)
    month_keyword.append(
        [
            InlineKeyboardButton(text="prev", callback_data="prev"),
            InlineKeyboardButton(text="Меню", callback_data="main"),
            InlineKeyboardButton(text="next", callback_data="next"),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=month_keyword)


async def generate_str(iterable, month: int) -> str:
    """
    Генерация сообщения с подробной информацией на каждый
    день об отработанных часах и заработанной сумме.
    :param iterable: Объект запроса к бд.
    :param month: Месяц зак который идет создание сообщения.
    :return: Строку для показа пользователю.
    """
    create_str: str = f"{hbold("Итог за ", month_tuple[month])}\n"

    one: List[int] = [0, 0, 0]
    two: List[int] = [0, 0, 0]
    total: List[int] = [0, 0, 0]

    for sal in iterable:
        total[0] += sal[0].base_hours + sal[0].overtime
        total[1] += sal[0].overtime
        total[2] += sal[0].earned

        if sal[0].period == 1:
            one[0] += sal[0].base_hours + sal[0].overtime
            one[1] += sal[0].overtime
            one[2] += sal[0].earned

        if sal[0].period == 2:
            two[0] += sal[0].base_hours + sal[0].overtime
            two[1] += sal[0].overtime
            two[2] += sal[0].earned

    create_str += f"{60 * "-"}\n"
    create_str += f"Период 1: "
    create_str += f"{hbold(one[0])}ч, {hbold(one[1])}ч, {one[2]:,.2f}₽\n"
    create_str += f"{60 * "-"}\n"
    create_str += f"Период 2: "
    create_str += f"{hbold(two[0])}ч, {hbold(two[1])}ч, {two[2]:,.2f}₽\n"
    create_str += f"{60 * "-"}\n"
    create_str += f"За месяц: "
    create_str += f"{hbold(total[0])}ч, {hbold(total[1])}ч, {total[2]:,.2f}₽\n"
    create_str += f"{60 * "-"}"
    return create_str


async def gen_message_for_choice_day(salary: Salary, choice_date: str):
    """
    Генерируем простое сообщения для пользователя.
    :param choice_date: Переданная дата из календаря.
    :param salary: Заработок за определенный день.
    :return: Сообщение для пользователя.
    """
    if not salary:
        return f"За дату {choice_date} нет данных."
    return (
        f"Дата: {choice_date}. \nВы отработали: {hbold(salary.base_hours + salary.overtime)} часов.\n"
        f"Заработали: {salary.earned:,.2f}₽."
    )


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
