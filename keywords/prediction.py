from datetime import timedelta, datetime as dt, datetime, date
from typing import List, Dict
from collections import defaultdict

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import MONTH_DATA

user_choices: Dict[int, List[str]] = defaultdict(list)
hour_choices: Dict[int, List[str]] = defaultdict(list)
choices_days: Dict[str, int] = {
    "Понедельник": 0,
    "Вторник": 1,
    "Среда": 2,
    "Четверг": 3,
    "Пятница": 4,
}


async def prediction_button() -> InlineKeyboardMarkup:
    """
    Генерирует инлайн-кнопки для выбора текущего и следующего месяца.

    Эта функция создает список списков кнопок для инлайн-клавиатуры, где
    каждая кнопка представляет собой месяц. Первая кнопка соответствует
    текущему месяцу, а вторая кнопка соответствует следующему месяцу.

    :return: Список списков объектов InlineKeyboardButton, представляющих
            кнопки для инлайн-клавиатуры.
    """
    year, month = datetime.now().year, datetime.now().month
    return  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"{MONTH_DATA[dt.now().month]}",
                callback_data="current",
            ),
            InlineKeyboardButton(
                text=f"{MONTH_DATA[(
                        date(year, month, 1) + timedelta(days=35)
                ).month]}",
                callback_data="next_month",
            ),
        ]
    ])


async def get_weekdays_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Генерирует инлайн-клавиатуру для выбора дней недели и часов.

    Эта асинхронная функция создает инлайн-клавиатуру, содержащую кнопки для
    выбора дней недели (Пн, Вт, Ср, Чт, Пт) и часов (1ч - 5ч). Кнопки
    отображают состояние выбора (выбрано или не выбрано) в зависимости от
    текущих выборов пользователя.

    :return: Объект InlineKeyboardMarkup, представляющий инлайн-клавиатуру с
                кнопками.
    """
    keyboard: List[List[InlineKeyboardButton]] = [[]]
    days: List[str] = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]

    for day in days:
        # Добавляем кнопку с состоянием
        button_text = f"[❌] {day[:2]}" if day not in user_choices[user_id] else f"[✅] {day[:2]}"
        keyboard[0].append(
            InlineKeyboardButton(text=button_text, callback_data=f"toggle_{day}")
        )

    button: List[InlineKeyboardButton] = []
    for i in range(1, 6):
        text = f"[❌] {i}ч" if str(i) not in hour_choices[user_id] else f"[✅] {i}ч"
        button.append(
            InlineKeyboardButton(text=text, callback_data=f"toggle_{i}")
        )

    keyboard.append(button)
    keyboard.append([
        InlineKeyboardButton(text="Завершить выбор", callback_data="finish"),
        InlineKeyboardButton(text="Меню", callback_data="main")
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


select_schedule_button: List[List[InlineKeyboardButton]] = [
    [
        InlineKeyboardButton(text="График 5/2", callback_data="five_days"),
        InlineKeyboardButton(text="График 2/2", callback_data="two_in_two")
    ]
]


select_schedule_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=select_schedule_button
)
