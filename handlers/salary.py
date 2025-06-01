from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold

from config import BOT_TOKEN
from handlers.bot_answer import decorator_errors
from keyboards.keyboard import back, menu
from crud.create import write_other
from states.salary import SalaryState

salary: Router = Router()
bot = Bot(token=BOT_TOKEN)


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
