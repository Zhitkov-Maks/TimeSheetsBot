from datetime import datetime
from typing import List, Tuple

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy import Row

from config import BOT_TOKEN
from crud.statistics import request_statistic
from handlers.bot_answer import decorator_errors
from keywords.keyword import menu
from keywords.statistics import keyword_statistic_year
from states.statistic import StatisticState
from utils.statistic import gen_message_statistic

statistic: Router = Router()
bot = Bot(token=BOT_TOKEN)


@statistic.callback_query(F.data == "statistic")
@decorator_errors
async def get_statistics(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик команды получения статистики. Показывает клавиатуру для
    выбора года.
    """
    await callback.message.delete_reply_markup()
    year: int = datetime.now().year
    await state.set_state(StatisticState.year)
    await callback.message.answer(
        text="Выберите год.",
        reply_markup=await keyword_statistic_year(year)
    )


@statistic.callback_query(StatisticState.year)
@decorator_errors
async def choice_year(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Показа статистики за выбранный год.
    """
    await callback.message.delete_reply_markup()
    year: int = int(callback.data)
    result: Row[List[Tuple[int]]] = await request_statistic(
        callback.from_user.id, year
    )
    await state.clear()
    if result[0] is not None:
        mess: str = await gen_message_statistic(result, year)

        await callback.message.answer(
            text=mess, parse_mode="HTML", reply_markup=menu
        )

    else:
        await callback.message.answer(
            text="За выбранный год нет данных.", reply_markup=menu
        )
