import re
from datetime import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from aiogram import Router
from aiogram import F
from aiogram.utils.markdown import hbold
from sqlalchemy import Sequence

from crud.statistics import get_information_for_month, get_info_by_date
from database.models import Salary
from keywords.keyword import menu, get_data_choices_day
from states.state import MonthState
from utils.genMessagePeriod import generate_str, create_calendar, \
    gen_message_for_choice_day, get_date

month_router = Router()
date_pattern = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$'


@month_router.callback_query(F.data == "month_current")
async def handle_info_current_month(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    """
    Обработчик для команды month_current. Получает информацию
    о текущем месяце.
    """
    year: int = datetime.now().year
    month: int = datetime.now().month
    result: Sequence = await get_information_for_month(
        callback.from_user.id,year, month)

    await state.set_state(MonthState.choice)
    await state.update_data(year=year, month=month)

    calendar: InlineKeyboardMarkup = await create_calendar(result, year, month)
    message: str = await generate_str(result, month - 1)

    await callback.message.answer(
        message,
        parse_mode="HTML"
    )
    await callback.message.answer(
        f"Календарь за - {hbold(month)}/{hbold(year)}",
        reply_markup=calendar,
        parse_mode="HTML"
    )


@month_router.callback_query(
    MonthState.choice,
    lambda callback_query: re.match(date_pattern, callback_query.data)
)
async def choice_day_on_month(
    callback: CallbackQuery,
    state: FSMContext
):
    choice_date = callback.data
    await state.update_data(date=choice_date)

    info_for_date: Salary | None = await get_info_by_date(callback.from_user.id, choice_date)
    message: str = await gen_message_for_choice_day(info_for_date)
    keyword: InlineKeyboardMarkup = await get_data_choices_day()

    await callback.message.answer(
        text=message,
        parse_mode="HTML",
        reply_markup=keyword
    )


@month_router.callback_query(F.data.in_(["next", "prev"]))
async def next_and_prev_month(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    data = await state.get_data()
    if len(data) != 0:
        year, month = await get_date(data, callback.data)

        result: Sequence = await get_information_for_month(
            callback.from_user.id,year, month
        )
        await state.update_data(year=year, month=month)
        await state.set_state(MonthState.choice)
        calendar: InlineKeyboardMarkup = await create_calendar(result, year, month)
        message: str = await generate_str(result, month - 1)

        await callback.message.answer(
            message,
            parse_mode="HTML"
        )

        await callback.message.answer(
            f"Календарь за - {hbold(month)}/{hbold(year)}",
            reply_markup=calendar,
            parse_mode="HTML"
        )
    else:
        await state.clear()
        await callback.message.answer(
            text="Информация о календаре устарела, обновите календарь "
                 "выбрав в меню текущий месяц.",
            reply_markup=await menu()
        )
