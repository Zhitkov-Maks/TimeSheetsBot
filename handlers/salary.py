from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold

from keyboards.keyboard import back_calendar, back_to_information
from crud.create import write_other, remove_other_income_expese
from crud.statistics import get_other_incomes_expenses
from states.salary import SalaryState
from utils.decorate import errors_logger
from utils.month import get_date
from utils.common import calculation_currency, parse_income_expense

salary: Router = Router()


@salary.callback_query(F.data.in_(["list_incomes", "list_expenses"]))
@errors_logger
async def get_list_transaction(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    """Show other income or expenses."""
    income: bool = False if callback.data == "list_expenses" else True
    data: dict = await state.get_data()
    year, month = data["year"], data["month"]
    result: list = await get_other_incomes_expenses(
        callback.from_user.id,
        year,
        month,
        income
    )
    message, next, prev, _id = await parse_income_expense(
        result, income, page=1
    )
    if message is None:
        await callback.answer(
            text="❌ Записей не найдено!",
            show_alert=True
        )
    else:
        await state.update_data(
            page=1, transaction=result, income=income, id=_id
        )
        await callback.message.edit_text(
            text=hbold(message),
            reply_markup=await back_to_information(next, prev),
            parse_mode="HTML"
        )


@salary.callback_query(F.data.in_(["next_tr", "prev_tr"]))
@errors_logger
async def next_page_transaction(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """Show the previous or next page."""
    data: dict = await state.get_data()
    page, result, income = data["page"], data["transaction"], data["income"]

    if callback.data == "next_tr":
        page += 1
    else:
        page -= 1

    message, next, prev, _id = await parse_income_expense(
        result, income, page=page
    )
    await state.update_data(page=page, id=_id)
    await callback.message.edit_text(
        text=hbold(message),
        reply_markup=await back_to_information(next, prev),
        parse_mode="HTML"
    )


@salary.callback_query(F.data == "remove_transaction")
@errors_logger
async def remove_transaction(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """Delete the transaction."""
    data: dict = await state.get_data()
    income, _id, year, month = (
        data["income"], data["id"], int(data["year"]), int(data["month"])
    )
    collections: str = "other_income" if income else "expences"
    await remove_other_income_expese(collections, _id)
    year, month = await get_date(data, data)
    result: list = await get_other_incomes_expenses(
        callback.from_user.id,
        year,
        month,
        income
    )
    message, next, prev, _id = await parse_income_expense(
        result, income, page=1
    )
    if message is None:
        await callback.message.edit_text(
            text=hbold("❌ Записей не найдено!"),
            reply_markup=back_calendar,
        )
    else:
        await state.update_data(
            page=1, transaction=result, income=income, id=_id
        )
        await callback.message.edit_text(
            text=hbold(message),
            reply_markup=await back_to_information(next, prev),
            parse_mode="HTML"
        )


@salary.callback_query(F.data.in_(["other_income", "expences"]))
@errors_logger
async def create_other_income(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    """Add other income or expense."""
    if callback.data == "other_income":
        await state.update_data(type_="income")
        text = "Введите сумму дохода 💴."
    else:
        await state.update_data(type_="expence")
        text = "Введите сумму расхода 💴."

    await state.set_state(SalaryState.amount)
    await callback.message.edit_text(
        text=hbold(text),
        reply_markup=back_calendar,
        parse_mode="HTML"
    )


@salary.message(SalaryState.amount)
@errors_logger
async def create_description_income(
    message: Message,
    state: FSMContext
) -> None:
    """Add a description to the transaction."""
    try:
        await state.update_data(amount=float(message.text))
        await state.set_state(SalaryState.description)
        await message.answer(
            text=hbold("Добвте описание 💬."),
            reply_markup=back_calendar,
            parse_mode="HTML"
        )

    except ValueError:
        await message.answer(
            text="Необходимо ввести число.",
            reply_markup=back_calendar
        )


@salary.message(SalaryState.description)
@errors_logger
async def write_other_income(
    message: Message,
    state: FSMContext
) -> None:
    """Save the transaction."""
    await state.update_data(description=message.text)
    data: dict = await state.get_data()
    valute_data = await calculation_currency(data.get("amount"))
    result: bool = await write_other(data, message.from_user.id, valute_data)

    if result:
        await message.answer(
            text=hbold("✅ Done."),
            reply_markup=back_calendar,
            parse_mode="HTML"
        )
    else:
        await message.answer(
            text=hbold("🪲 Данных не найдено."),
            reply_markup=back_calendar,
            parse_mode="HTML"
        )
