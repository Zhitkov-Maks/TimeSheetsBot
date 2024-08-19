from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from decouple import config
from datetime import datetime as dt

import os

from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

BOT_TOKEN = config("TOKEN")

month_tuple = (
    "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
    "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь",
)

weekdays = ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")

menu_bot = [
    [
        InlineKeyboardButton(
            text=f"{month_tuple[dt.now().month - 1]}/Посмотреть",
            callback_data="month_current"
        ),
        InlineKeyboardButton(
            text=f"{month_tuple[dt.now().month - 2]}/Посмотреть",
            callback_data="month_prev"
        )],
    [
        InlineKeyboardButton(
            text="Добавить доход", callback_data="select_date"
        ),
        InlineKeyboardButton(
            text="Заработано за...", callback_data="period"
        ),
    ],
    [
        InlineKeyboardButton(
            text="Калькулятор", callback_data="calc"
        ),
        InlineKeyboardButton(
            text="Сегодня", callback_data="today"
        ),
    ]
]

confirm = [
    [InlineKeyboardButton(
        text="Отмена",
        callback_data="help"
    ),
        InlineKeyboardButton(
            text="Продолжить",
            callback_data="continue"
        )]
]

mail = [
    [
        InlineKeyboardButton(
            text="Мой телеграм",
            url='tg://resolve?domain=Maksim1Zhitkov'
        ),
        InlineKeyboardButton(
            text="Закрыть",
            callback_data="help"
        )
    ]
]

confirm_menu = InlineKeyboardMarkup(inline_keyboard=confirm)
mail_menu = InlineKeyboardMarkup(inline_keyboard=mail)
menu = InlineKeyboardMarkup(inline_keyboard=menu_bot)
