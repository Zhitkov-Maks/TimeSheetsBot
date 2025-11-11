from datetime import datetime, UTC

from aiogram.types import CallbackQuery, Message
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold

from crud.statistics import statistics_for_year, get_other_incomes_for_year
from keyboards.keyboard import next_prev_year
from loader import CURRENCY_SYMBOL
from utils.statistic import generate_message_statistic, sum_currency


statistick_router = Router()


@statistick_router.message(F.text == "/stat")
async def get_current_year_statistics(
    message: Message, state: FSMContext
) -> None:
    """Show the statistics for the selected year."""
    year: int = datetime.now(UTC).year

    result_for_hours: dict = await statistics_for_year(
        year, message.from_user.id
    )
    result_for_other: dict = await get_other_incomes_for_year(
        message.from_user.id, year
    )
    currency = await sum_currency(result_for_hours, result_for_other)
    mess: str = await generate_message_statistic(
        result_for_hours, result_for_other, year
    )

    await state.update_data(year=year, valute_data_year=currency)
    await message.answer(
        text=hbold(mess),
        reply_markup=await next_prev_year(year),
        parse_mode="HTML"
    )


@statistick_router.callback_query(F.data.in_(["prev_year", "next_year"]))
async def get_prev_next_year_statistics(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """Show the statistics for the previous month."""
    year: int = (await state.get_data()).get("year")
    if callback.data == "prev_year":
        year -= 1

    elif callback.data == "next_year":
        year += 1
    
    else:
        year = datetime.now().year

    result_for_hours: dict = await statistics_for_year(
        year, callback.from_user.id
    )
    result_for_other: dict = await get_other_incomes_for_year(
        year, callback.from_user.id
    )
    currency = await sum_currency(result_for_hours, result_for_other)
    message: str = await generate_message_statistic(
        result_for_hours, result_for_other, year
    )

    await state.update_data(year=year, valute_data_year=currency)
    await callback.message.edit_text(
        text=hbold(message),
        reply_markup=await next_prev_year(year),
        parse_mode="HTML"
    )


@statistick_router.callback_query(
    F.data.in_(["dollar_y", "euro_y", "yena_y", "som_y"])
)
async def get_earned_in_valute_for_month(
    callback: CallbackQuery, 
    state: FSMContext
) -> None:
    """
    Show the user the data of his earnings 
    in the currency of month.
    """
    data: dict[str, str | int] = await state.get_data()
    name: str = callback.data.split("_")[0]
    valute = data.get("valute_data_year")
    if valute:
        await callback.answer(
            text=f"{valute[name]:,}{CURRENCY_SYMBOL[name]}",
            show_alert=True
        )
