from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold

from handlers.bot_answer import decorator_errors
from keyboards.keyboard import back, menu, back_to_information
from crud.create import write_other
from crud.statistics import get_other_incomes_expenses
from states.salary import SalaryState
from utils.month import get_date
from utils.common import parse_income_expense

salary: Router = Router()


@salary.callback_query(F.data.in_(["list_incomes", "list_expenses"]))
@decorator_errors
async def get_list_transaction(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    """Обработчик просмотра прочих доходов и списаний(Штрафы и т.д)."""
    income = False if callback.data == "list_expenses" else True
    data = await state.get_data()
    year, month = await get_date(data, data)
    result = await get_other_incomes_expenses(
        callback.from_user.id,
        year,
        month,
        income
    )
    message: str = await parse_income_expense(result, income)
    await callback.message.edit_text(
        text=hbold(message),
        reply_markup=await back_to_information(),
        parse_mode="HTML"
    )


@salary.callback_query(F.data.in_(["other_income", "expences"]))
@decorator_errors
async def create_other_income(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    """Обработчик добавления прочего дохода."""
    if callback.data == "other_income":
        await state.update_data(type_="income")
        text = "Введите сумму прочего дохода"
    else:
        await state.update_data(type_="expence")
        text = "Введите сумму расхода"

    await state.set_state(SalaryState.amount)
    await callback.message.answer(
        text=text,
        reply_markup=back,
        parse_mode="HTML"
    )


@salary.message(SalaryState.amount)
async def create_description_income(
    message: Message,
    state: FSMContext
) -> None:
    try:
        await state.update_data(amount=float(message.text))
        await state.set_state(SalaryState.description)
        await message.answer(
            text="Добвте небольшое описание:",
            reply_markup=back,
            parse_mode="HTML"
        )

    except ValueError:
        await message.answer(
            text="Необходимо ввести число.",
            reply_markup=back
        )


@salary.message(SalaryState.description)
async def write_other_income(
    message: Message,
    state: FSMContext
) -> None:
    await state.update_data(description=message.text)
    data = await state.get_data()
    result = await write_other(data, message.from_user.id)
    if result:
        await message.answer(
            text="Запись успешно добавлена.",
            reply_markup=menu
        )
    else:
        await message.answer(
            text="Произошел сбой, попробуйте еще раз",
            reply_markup=menu
        )
