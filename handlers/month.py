import re
from datetime import datetime
from typing import Dict

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from aiogram import Router, Bot
from aiogram import F
from sqlalchemy import Sequence

from config import BOT_TOKEN
from crud.statistics import get_information_for_month, get_info_by_date
from database.models import Salary
from handlers.bot_answer import sent_calendar
from keywords.keyword import menu, get_data_choices_day
from loader import date_pattern
from states.state import MonthState
from utils.gen_message_period import (
    gen_message_for_choice_day,
    get_date,
)

month_router = Router()
bot = Bot(token=BOT_TOKEN)


@month_router.callback_query(F.data == "month_current")
async def handle_info_current_month(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик для команды month_current. Получает информацию
    о текущем месяце.
    """
    await callback.message.delete_reply_markup()
    year: int = datetime.now().year
    month: int = datetime.now().month
    result: Sequence = await get_information_for_month(
        callback.from_user.id, year, month
    )

    await state.set_state(MonthState.choice)
    await state.update_data(year=year, month=month)
    await sent_calendar(year, month, result, callback.from_user.id)


@month_router.callback_query(
    MonthState.choice,
    lambda callback_query: re.match(date_pattern, callback_query.data),
)
async def choice_day_on_month(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает выбранный день в календаре.
    """
    choice_date: str = callback.data
    await state.update_data(date=choice_date)

    info_for_date: Salary | None = await get_info_by_date(
        callback.from_user.id, choice_date
    )
    message: str = await gen_message_for_choice_day(info_for_date, choice_date)
    keyword: InlineKeyboardMarkup = await get_data_choices_day(info_for_date)

    await callback.message.answer(text=message, parse_mode="HTML", reply_markup=keyword)


@month_router.callback_query(F.data.in_(["next", "prev"]))
async def next_and_prev_month(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает команды на предыдущий или следующий месяц.
    """
    await callback.message.delete_reply_markup()
    data: Dict[str, str | int] = await state.get_data()

    if len(data) != 0:
        year, month = await get_date(data, callback.data)

        result: Sequence = await get_information_for_month(
            callback.from_user.id, year, month
        )
        await state.update_data(year=year, month=month)
        await state.set_state(MonthState.choice)
        await sent_calendar(year, month, result, callback.from_user.id)

    else:
        await state.clear()
        await callback.message.answer(
            text="Информация о календаре устарела, обновите календарь "
            "выбрав в меню текущий месяц.",
            reply_markup=await menu(),
        )
