from typing import List
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def keyword_statistic_year(year: int) -> InlineKeyboardMarkup:
    """
    Функция для получения годов для выбора в статистике.
    :param year: Текущий год.
    :return InlineKeyboardMarkup: Инлайн клавиатуру.
    """
    keyword: List[List[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(text=f"{year} г", callback_data=str(year)),
            InlineKeyboardButton(text=f"{year - 1} г",
                                 callback_data=str(year - 1)),
            InlineKeyboardButton(text=f"{year - 2} г.",
                                 callback_data=str(year - 2)),
        ],
        [InlineKeyboardButton(text="Показать меню", callback_data="main")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyword)
