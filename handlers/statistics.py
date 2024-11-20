from datetime import datetime
from typing import List

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import hbold
from sqlalchemy import Row

from crud.statistics import request_statistic
from keywords.keyword import menu
from states.state import StatisticState

statistic: Router = Router()


@statistic.callback_query(F.data == "statistic")
async def get_statistics(callback: CallbackQuery, state: FSMContext) -> None:
    """Обработчик команды получения статистики. Показывает клавиатуру для
    выбора года.
    """
    await callback.message.delete_reply_markup(inline_message_id=callback.id)
    year: int = datetime.now().year
    keyword: List[List[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(text=str(year), callback_data=str(year)),
            InlineKeyboardButton(text=str(year - 1), callback_data=str(year - 1)),
            InlineKeyboardButton(text=str(year - 2), callback_data=str(year - 2)),
        ]
    ]
    await state.set_state(StatisticState.year)
    await callback.message.answer(
        text="Выберите год.", reply_markup=InlineKeyboardMarkup(inline_keyboard=keyword)
    )


@statistic.callback_query(StatisticState.year)
async def choice_year(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Показа статистики за выбранный год.
    """
    await callback.message.delete_reply_markup(inline_message_id=callback.id)
    year: int = int(callback.data)
    result: Row[tuple] = await request_statistic(callback.from_user.id, year)
    if result[0] is not None:
        mess: str = (
            f"Ваша статистика за {hbold(year)} год."
            f"Заработано: {hbold(result[0])}₽\n"
            f"Отработано часов: {hbold(result[1] + result[2])}ч\n"
            f"Из них переработки: {hbold(result[2])}ч."
        )
        await callback.message.answer(
            text=mess, parse_mode="HTML", reply_markup=await menu()
        )
    else:
        await state.clear()
        await callback.message.answer(
            text="За выбранный год нет данных.", reply_markup=await menu()
        )
