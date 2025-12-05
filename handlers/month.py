import re
from datetime import datetime
from typing import Dict

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest
from aiogram import Router
from aiogram import F
from aiogram.utils.markdown import hbold
from crud.statistics import get_information_for_month, get_info_by_date
from keyboards.current_day import get_data_choices_day
from keyboards.month import create_calendar, get_month_menu
from loader import CURRENCY_SYMBOL, MONTH_DATA, date_pattern
from states.month import MonthState
from utils.current_day import gen_message_for_choice_day
from utils.decorate import errors_logger
from utils.month import get_date, generate_str
from utils.month import (
    get_amount_and_hours_for_month,
    get_message_for_period
)
from utils.valute import get_valute_for_month

month_router = Router()


@month_router.message(F.text == "/main")
@errors_logger
async def handle_info_current_month(
    message: Message,
    state: FSMContext
) -> None:
    """Show the calendar for the current month."""
    year: int = datetime.now().year
    month: int = datetime.now().month
    result = await get_information_for_month(
        message.from_user.id, year, month
    )

    data: tuple[tuple] = (
        await get_amount_and_hours_for_month(
            year, month, message.from_user.id, state
        )
    )

    await state.set_state(MonthState.choice)
    await state.update_data(year=year, month=month, result=result)
    await message.answer(
        text=hbold(f"{MONTH_DATA[month]} {year}г"),
        reply_markup=await create_calendar(result, year, month, data),
        parse_mode="HTML"
    )


@month_router.callback_query(
    MonthState.choice,
    lambda callback_query: re.match(date_pattern, callback_query.data),
)
@errors_logger
async def choice_day_on_month(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    """
    Show me the information for the day.
    """
    choice_date: str = callback.data
    info_for_date = await get_info_by_date(
        callback.from_user.id, choice_date
    )
    await state.update_data(current_day=info_for_date, date=choice_date)
    message: str = await gen_message_for_choice_day(
        info_for_date, choice_date
    )
    await callback.message.edit_text(
        text=hbold(message),
        parse_mode="HTML",
        reply_markup=await get_data_choices_day(info_for_date)
    )


@month_router.callback_query(F.data == "calendar")
@errors_logger
async def show_monthly_data(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    """
    Show the information for the month.
    """
    data: Dict[str, str | int] = await state.get_data()
    year, month = await get_date(data, callback.data)
    message: str = await generate_str(year, month, callback.from_user.id)
    
    await callback.message.edit_text(
        hbold(message),
        reply_markup=await get_month_menu(),
        parse_mode="HTML"
    )


@month_router.callback_query(F.data.in_(["next", "prev", "current"]))
@errors_logger
async def next_and_prev_month(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    """
    Show the previous or next month.
    """
    data: Dict[str, str | int] = await state.get_data()
    year, month = await get_date(data, callback.data)
    result: list = await get_information_for_month(
        callback.from_user.id, year, month
    )
    await state.update_data(year=year, month=month, result=result)
    await state.set_state(MonthState.choice)
    
    data: tuple = (
        await get_amount_and_hours_for_month(
            year, month, callback.from_user.id, state
        )
    )
    text = text=hbold(f"{MONTH_DATA[month]} {year}г")
    try:
        await callback.message.edit_text(
            text=text,
            reply_markup=await create_calendar(result, year, month, data),
            parse_mode="HTML"
        )
    except TelegramBadRequest:
        await callback.message.answer(
            text=text,
            reply_markup=await create_calendar(result, year, month, data),
            parse_mode="HTML"
        )


@month_router.callback_query(
    F.data.in_(["dollar_m", "euro_m", "yena_m", "som_m"])
)
@errors_logger
async def get_earned_in_valute_for_month(
    callback: CallbackQuery, 
    state: FSMContext
) -> None:
    """
    Show the user the data of his earnings 
    in the currency of month.
    """
    data: Dict[str, str | int] = await state.get_data()
    name: str = callback.data.split("_")[0]
    year, month = data.get("year"), data.get("month")

    text: str = await get_valute_for_month(
        year, month, callback.from_user.id, name
    )
    await callback.answer(
        text=text,
        show_alert=True
    )


@month_router.callback_query(
    F.data.in_(["period1", "period2", "total_amount"])
)
@errors_logger
async def get_information_for_period(
    callback: CallbackQuery,
    state: FSMContext
 ) -> None:
    """Show more detailed information for the period or month."""
    data: dict = await state.get_data()
    period: str = callback.data
    if "total" not in period:
         data_ = data.get(period)
    else:
        data_ = data.get("for_month")
        
    mess: str = await get_message_for_period(data_, period)
    await callback.answer(
         text=mess,
         show_alert=True,
    )
