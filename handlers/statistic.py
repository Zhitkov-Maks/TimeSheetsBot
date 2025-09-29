from datetime import datetime, UTC

from aiogram.types import CallbackQuery
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold

from crud.statistics import statistics_for_year, get_other_incomes_for_year
from keyboards.keyboard import next_prev_year
from utils.statistic import generate_message_statistic


statistick_router = Router()


@statistick_router.callback_query(F.data == "statistics")
async def get_current_year_statistics(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """Покажи статистику за текущий месяц."""
    year: int = datetime.now(UTC).year

    result_for_hours: dict = await statistics_for_year(
        year, callback.from_user.id
    )
    result_for_other: dict = await get_other_incomes_for_year(
        callback.from_user.id, year
    )
    message: str = await generate_message_statistic(
        result_for_hours, result_for_other, year
    )

    await state.update_data(year=year)
    await callback.message.answer(
        text=hbold(message),
        reply_markup=await next_prev_year(year),
        parse_mode="HTML"
    )


@statistick_router.callback_query(F.data.in_(["prev_year", "next_year"]))
async def get_prev_next_year_statistics(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """Покажи статистику за предыдущий месяц."""
    year: int = (await state.get_data())["year"]
    if callback.data == "prev_year":
        year -= 1
    else:
        year += 1

    result_for_hours: dict = await statistics_for_year(
        year, callback.from_user.id
    )
    result_for_other: dict = await get_other_incomes_for_year(
        year, callback.from_user.id
    )
    message: str = await generate_message_statistic(
        result_for_hours, result_for_other, year
    )
    await state.update_data(year=year)
    await callback.message.answer(
        text=hbold(message),
        reply_markup=await next_prev_year(year),
        parse_mode="HTML"
    )
