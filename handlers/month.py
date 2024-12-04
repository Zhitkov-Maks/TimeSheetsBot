import re
from datetime import datetime
from typing import Dict

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import Router, Bot
from aiogram import F
from sqlalchemy import Sequence, Row

from config import BOT_TOKEN
from crud.statistics import get_information_for_month, get_info_by_date
from database.models import Salary
from keywords.current_day import get_data_choices_day
from keywords.keyword import menu
from keywords.month import create_calendar
from loader import date_pattern
from states.month import MonthState
from utils.current_day import gen_message_for_choice_day
from utils.month import get_date, generate_str

month_router = Router()
bot = Bot(token=BOT_TOKEN)


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
        callback.from_user.id, year, month
    )

    await state.set_state(MonthState.choice)
    await state.update_data(year=year, month=month, result=result)
    await callback.message.answer(
        text="...",
        reply_markup=await create_calendar(result, year, month)
    )
    await callback.message.delete()


@month_router.callback_query(
    MonthState.choice,
    lambda callback_query: re.match(date_pattern, callback_query.data),
)
async def choice_day_on_month(
        callback: CallbackQuery,
        state: FSMContext
) -> None:
    """
    Обрабатывает выбранный день в календаре.
    """
    choice_date: str = callback.data
    await state.update_data(date=choice_date)
    info_for_date: Salary | None = await get_info_by_date(
        callback.from_user.id, choice_date
    )
    message: str = await gen_message_for_choice_day(info_for_date, choice_date)
    user_data = await state.get_data()

    last_choice_date = user_data.get("last_choice_date")

    if last_choice_date == choice_date:
        # Если дата была выбрана ранее, отправляем сообщение
        await callback.message.answer(
            text=message,
            parse_mode="HTML",
            reply_markup=await get_data_choices_day(info_for_date)
        )
        await state.update_data(last_choice_date=None)
    else:
        # Если это новое нажатие, просто отвечаем на callback с сообщением
        await callback.answer(message, show_alert=True)
        # Обновляем последнюю выбранную дату в состоянии
        await state.update_data(last_choice_date=choice_date)


@month_router.callback_query(F.data == "calendar")
async def show_monthly_data(
        callback: CallbackQuery,
        state: FSMContext
) -> None:
    data: Dict[str, str | int] = await state.get_data()
    month: int = data.get("month")
    result: Sequence[Row[tuple[Salary]]] = data.get("result")
    message: str = await generate_str(result, month)
    await callback.answer(message, show_alert=True)


@month_router.callback_query(F.data.in_(["next", "prev"]))
async def next_and_prev_month(
        callback: CallbackQuery,
        state: FSMContext
) -> None:
    """
    Обрабатывает команды на предыдущий или следующий месяц.
    """
    data: Dict[str, str | int] = await state.get_data()
    if len(data) != 0:
        year, month = await get_date(data, callback.data)

        result: Sequence = await get_information_for_month(
            callback.from_user.id, year, month
        )
        await state.update_data(year=year, month=month, result=result)
        await state.set_state(MonthState.choice)
        await callback.message.edit_reply_markup(
            reply_markup=await  create_calendar(result, year, month)
        )

    else:
        await state.clear()
        await callback.message.answer(
            text="Некорректный ввод. Попробуйте еще раз.",
            reply_markup=menu,
        )
