from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram import F

from crud.create import get_total_salary
from keywords.keyword import menu, month_menu, \
    month_data, year_menu, get_year_date
from states.state import PeriodState
from utils.statistics import total_info

period_router = Router()

month_dict = {
    "january": "01", "february": "02", "mart": "03", "april": "04",
    "mai": "05", "june": "06", "july": "07", "august": "08",
    "september": "09", "oktober": "10", "november": "11", "december": "12"
}


@period_router.callback_query(F.data == "period")
async def on_year_selected(
        callback: CallbackQuery, state: FSMContext
) -> None:
    """Обрабатывает команду period. Запрашивает год."""
    await state.set_state(PeriodState.year)
    await callback.message.answer(
        text="Укажите год",
        reply_markup=await year_menu()
    )


@period_router.callback_query(F.data.in_(get_year_date()), PeriodState.year)
async def on_month_selected(
        callback: CallbackQuery, state: FSMContext
) -> None:
    """Показывает реплэй клавиатуру для выбора месяца."""
    await state.set_state(PeriodState.month)
    await state.update_data(year=callback.data)
    await callback.message.answer(
        text="Укажите месяц",
        reply_markup=await month_menu()
    )


@period_router.callback_query(F.data.in_(month_data), PeriodState.month)
async def on_date_selected(
        callback: CallbackQuery, state: FSMContext
) -> None:
    """
    Запрашивает данные в базе для введенных пользователем данных.
    """
    await state.update_data(
        month=month_dict.get(callback.data)
    )
    data = await state.get_data()
    one, two, total = await get_total_salary(
        data["year"],
        data["month"],
        callback.from_user.id
    )
    text: str = await total_info(one, two, total)
    await callback.message.answer(
        text=text,
        parse_mode="HTML",
        reply_markup=await menu()
    )
    await state.clear()
