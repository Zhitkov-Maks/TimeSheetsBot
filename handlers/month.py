import re
from datetime import datetime
from typing import Dict

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram import F
from aiogram.utils.markdown import hbold
from crud.statistics import get_information_for_month, get_info_by_date
from handlers.bot_answer import decorator_errors
from keyboards.current_day import get_data_choices_day
from keyboards.month import create_calendar, get_month_menu
from loader import date_pattern
from states.month import MonthState
from utils.current_day import gen_message_for_choice_day
from utils.month import get_date, generate_str

month_router = Router()


@month_router.callback_query(F.data == "month_current")
@decorator_errors
async def handle_info_current_month(
        callback: CallbackQuery,
        state: FSMContext
) -> None:
    """
    Обработчик для команды month_current. Получает информацию
    о текущем месяце и формирует календарь пользователю, в котором
    отмечены его смены.
    """
    year: int = datetime.now().year
    month: int = datetime.now().month
    result = await get_information_for_month(
        callback.from_user.id, year, month
    )

    await state.set_state(MonthState.choice)
    await state.update_data(year=year, month=month, result=result)
    await callback.message.edit_text(
        text=f"Ваши данные за {month}/{year}",
        reply_markup=await create_calendar(result, year, month),
        parse_mode="HTML"
    )


@month_router.callback_query(
    MonthState.choice,
    lambda callback_query: re.match(date_pattern, callback_query.data),
)
@decorator_errors
async def choice_day_on_month(
        callback: CallbackQuery,
        state: FSMContext
) -> None:
    """
    Обрабатывает выбранный день в календаре. При первом нажатии показывает
    уведомление с данными за выбранный день, при повторном нажатии показывает
    сообщение с данными и предложением добавить, изменить или удалить данные.
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
        text=message,
        parse_mode="HTML",
        reply_markup=await get_data_choices_day(info_for_date)
    )


@month_router.callback_query(F.data == "calendar")
@decorator_errors
async def show_monthly_data(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    """
    Обработчик кнопки при нажатии на месяц в календаре. Показывает общую
    информацию за выбранный месяц в виде сообщения.
    """
    data: Dict[str, str | int] = await state.get_data()
    year, month = data.get("year"), data.get("month")
    message: str = await generate_str(year, month, callback.from_user.id)
    await callback.message.edit_text(
        hbold(message),
        reply_markup=await get_month_menu(),
        parse_mode="HTML"
    )


@month_router.callback_query(F.data.in_(["next", "prev", "current"]))
@decorator_errors
async def next_and_prev_month(
        callback: CallbackQuery,
        state: FSMContext
) -> None:
    """
    Обрабатывает команды на предыдущий или следующий месяц. Формирует календари
    в зависимости от месяца.
    """
    data: Dict[str, str | int] = await state.get_data()
    year, month = await get_date(data, callback.data)
    result = await get_information_for_month(
        callback.from_user.id, year, month
    )
    await state.update_data(year=year, month=month, result=result)
    await state.set_state(MonthState.choice)
    await callback.message.edit_text(
        text=f"Ваши данные за {month}/{year}",
        reply_markup=await create_calendar(result, year, month)
    )
