from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup
from aiogram import Router
from aiogram import types, F

from crud.create import get_total_salary
from keywords.keyword import year_list, month_list, menu
from states.state import PeriodState
from utils.statistics import total_info

period_router = Router()


month_dict = {
    "январь": "01", "февраль": "02", "март": "03", "апрель": "04",
    "май": "05", "июнь": "06", "июль": "07", "август": "08",
    "сентябрь": "09", "октябрь": "10", "ноябрь": "11", "декабрь": "12"
}


@period_router.callback_query(F.data == "period")
async def on_year_selected(
        callback: CallbackQuery, state: FSMContext
) -> None:
    """Обрабатывает команду period. Запрашивает год."""
    await state.set_state(PeriodState.year)
    keyword = ReplyKeyboardMarkup(
        keyboard=year_list,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await callback.message.answer(
        text="Укажите год",
        reply_markup=keyword
    )


@period_router.message(F.text, PeriodState.year)
async def on_month_selected(
        message: types.Message, state: FSMContext
) -> None:
    """Показывает реплэй клавиатуру для выбора месяца."""
    await state.set_state(PeriodState.month)
    await state.update_data(year=message.text)
    keyword = ReplyKeyboardMarkup(
        keyboard=month_list,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(
        text="Укажите месяц",
        reply_markup=keyword
    )


@period_router.message(F.text, PeriodState.month)
async def on_date_selected(
        message: types.Message, state: FSMContext
) -> None:
    """
    Запрашивает данные в базе для введенных пользователем данных.
    """
    await state.update_data(month=month_dict.get(message.text.lower()))
    data = await state.get_data()
    one, two, total = await get_total_salary(
        data["year"],
        data["month"],
        message.from_user.id
    )
    text: str = await total_info(one, two, total)
    await message.answer(
        text=text,
        parse_mode="HTML",
        reply_markup=menu
    )
    await state.clear()
