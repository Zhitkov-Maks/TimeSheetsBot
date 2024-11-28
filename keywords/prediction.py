from datetime import timedelta, datetime as dt
from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keywords.keyword import month_tuple

user_choices = []
hour_choices = []
choices_days = {
    "Пн": 0,
    "Вт": 1,
    "Ср": 2,
    "Чт": 3,
    "Пт": 4,
}


def prediction_button() -> List[List[InlineKeyboardButton]]:
    return [
        [
            InlineKeyboardButton(
                text=f"{month_tuple[dt.now().month]}/Посчитать",
                callback_data="current",
            ),
            InlineKeyboardButton(
                text=f"{month_tuple[(dt.now() + timedelta(days=30)).month]}/Посчитать",
                callback_data="next_month",
            ),
        ]
    ]


async def prediction() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=prediction_button())


select_schedule_button: List[List[InlineKeyboardButton]] = [
    [
        InlineKeyboardButton(text="График 5/2", callback_data="five_days"),
        InlineKeyboardButton(text="График 2/2", callback_data="two_in_two")
    ]
]

select_schedule_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=select_schedule_button)

delay_button: List[List[InlineKeyboardButton]] = [
    [
        InlineKeyboardButton(text="Да Вт/Чт/2ч", callback_data="2/2"),
        InlineKeyboardButton(text="Да Вт/Чт/3ч", callback_data="2/3"),
        InlineKeyboardButton(text="Да Пн-Ср/3ч", callback_data="3/3"),
    ],
    [
        InlineKeyboardButton(text="Нет", callback_data="delay_no"),
        InlineKeyboardButton(text="Отмена", callback_data="main"),
    ]
]

delay_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=delay_button)


async def get_weekdays_keyboard():
    keyboard = [[]]
    days = ["Пн", "Вт", "Ср", "Чт", "Пт"]

    for day in days:
        # Добавляем кнопку с состоянием
        button_text = f"[❌] {day}" if day not in user_choices else f"[✅] {day}"
        keyboard[0].append(InlineKeyboardButton(text=button_text,
                                                callback_data=f"toggle_{day}"))
    button_two_overtime = f"[❌] Переработка 2ч" if "2" not in hour_choices else f"[✅] Переработка 2ч"
    button_three_overtime = f"[❌] Переработка 3ч" if "3" not in hour_choices else f"[✅] Переработка 3ч"
    keyboard.append([
        InlineKeyboardButton(text=button_two_overtime,
                             callback_data="toggle_2"),
        InlineKeyboardButton(text=button_three_overtime,
                             callback_data="toggle_3")
    ])

    keyboard.append([
        InlineKeyboardButton(text="Завершить выбор", callback_data="finish"),
        InlineKeyboardButton(text="Меню", callback_data="main")
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
