from typing import List, Dict

from aiogram import Router, Bot
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import BOT_TOKEN
from crud.create import delete_record, add_other_income
from handlers.bot_answer import send_calendar_and_message, processing_data
from keywords.keyword import cancel_button
from loader import add_record_text
from states.current_day import CreateState
from utils.current_day import split_data

create_router = Router()
bot = Bot(token=BOT_TOKEN)


@create_router.callback_query(F.data.in_(["change", "add"]))
async def on_date_today(callback: CallbackQuery, state: FSMContext) -> None:
    """Обработчик команд для добавления или изменения записи о смене."""
    await state.update_data(action=callback.data, callback=callback.id)
    await state.set_state(CreateState.check_data)
    await callback.message.answer(
        text=add_record_text, reply_markup=cancel_button)


@create_router.message(CreateState.check_data)
async def check_data(message: types.Message, state: FSMContext) -> None:
    """
    Сохранение и проверка введенного отработанного времени.
    """
    await state.update_data(user_id=message.from_user.id)
    data: Dict[str, str | float] = await state.get_data()
    numbers: List[str] = message.text.split("*")
    try:
        if len(numbers) == 1 or len(numbers) == 2:
            time, overtime = await split_data(numbers)
            await processing_data(
                message.from_user.id, time, overtime, state, data
            )
        else:
            raise ValueError

    except ValueError:
        await message.reply(
            "Введенные данные не соответствуют требованиям. \n"
            "Пример: 6.5*5. Попробуйте еще раз.",
            reply_markup=cancel_button,
        )


@create_router.callback_query(F.data == "bonus")
async def add_other_surcharges(callback: CallbackQuery,
                               state: FSMContext) -> None:
    await state.set_state(CreateState.other_income)
    await callback.message.answer(
        text="Введите сумму прочего дохода, сюда можно добавить например "
             "доплату за ночные часы, акционные доплаты и т.п.",
        reply_markup=cancel_button)


@create_router.message(CreateState.other_income)
async def update_other_income(message: Message, state: FSMContext):
    try:
        income: float = float(message.text)
        await state.update_data(user_id=message.from_user.id)
        data: dict = await state.get_data()
        await add_other_income(income, data)
        await send_calendar_and_message(message.from_user.id, data, state)
    except ValueError:
        await message.reply(
            "Ошибка ввода, необходимо вводить либо целые числа, "
            "либо числа с точкой, например 555.55"
        )


@create_router.callback_query(F.data == "del")
async def delete_record(callback: CallbackQuery, state: FSMContext) -> None:
    """Отправка на удаление записи."""
    await state.update_data(user_id=callback.from_user.id)
    data: Dict[str, str] = await state.get_data()

    await delete_record(data)
    await callback.answer("Запись удалена!!!")
    await send_calendar_and_message(callback.from_user.id, data, state)
