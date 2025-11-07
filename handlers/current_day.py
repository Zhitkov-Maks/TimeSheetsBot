from typing import Dict

from aiogram import Router, Bot
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold

from config import BOT_TOKEN
from crud.create import delete_record
from handlers.bot_answer import (
    send_calendar_and_message,
    processing_data,
    decorator_errors
)
from keyboards.keyboard import cancel_button, back
from loader import add_record_text, CURRENCY_SYMBOL
from states.current_day import CreateState
from utils.current_day import valid_time, earned_for_award
from utils.current_day import gen_message_for_choice_day
from utils.valute import gen_text
from keyboards.current_day import get_data_choices_day

day_router = Router()
bot = Bot(token=BOT_TOKEN)


@day_router.callback_query(F.data.in_(["change", "add"]))
@decorator_errors
async def on_date_today(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Ask the user for the number of hours worked.
    """
    await state.update_data(action=callback.data, callback=callback.id)
    await state.set_state(CreateState.check_data)
    await callback.message.edit_text(
        text=add_record_text, reply_markup=cancel_button
    )


@day_router.message(CreateState.check_data)
@decorator_errors
async def check_data(message: Message, state: FSMContext) -> None:
    """
    Save the data entered by the user if the data is correct.
    """
    await state.update_data(user_id=message.from_user.id)
    data: Dict[str, str | float] = await state.get_data()
    try:
        time: float = await valid_time(message.text)
        await processing_data(
            message.from_user.id, time, state, data
        )

    except ValueError:
        await message.reply(
            text=hbold("Некорректные данные. Попробуйте еще раз"),
            reply_markup=cancel_button,
            parse_mode="HTML"
        )

    except KeyError as err:
        await message.answer(
            text=hbold(str(err)),
            reply_markup=back,
            parse_mode="HTML"
        )


@day_router.callback_query(F.data == "del")
@decorator_errors
async def del_record(callback: CallbackQuery, state: FSMContext) -> None:
    """Delete the entries for the selected day."""
    await state.update_data(user_id=callback.from_user.id)
    data: Dict[str, str] = await state.get_data()

    await delete_record(data.get("date"), callback.from_user.id)
    await callback.answer("Запись удалена!!!")
    await send_calendar_and_message(callback.from_user.id, data, state)


@day_router.callback_query(F.data == "award")
@decorator_errors
async def add_award(callback: CallbackQuery, state: FSMContext) -> None:
    """Delete the entries for the selected day."""
    await state.set_state(CreateState.award)
    await callback.message.answer(
        text=hbold("Введите количество выполненных операций за смену: "),
        reply_markup=cancel_button,
        parse_mode="HTML"
    )


@day_router.message(CreateState.award)
@decorator_errors
async def create_award(message: Message, state: FSMContext) -> None:
    """Save the data if the data is correct."""
    try:
        count_operation: int = int(message.text)
        data: dict = await state.get_data()
        current_id: str = data.get("current_day").get("_id")
        date_, info_for_date = data.get("date"), data.get("current_day")
        
        update_current_day: dict = await earned_for_award(
            count_operation,
            message.from_user.id,
            current_id
        )
        await state.update_data(current_day=update_current_day)
        text: str = await gen_message_for_choice_day(
            update_current_day, date_
        )
        await message.answer(
            text=text,
            parse_mode="HTML",
            reply_markup=await get_data_choices_day(info_for_date)
        )

    except TypeError:
        await message.answer(
            text=hbold("Неверный ввод, нужно ввести целое число!"),
            reply_markup=cancel_button,
            parse_mode="HTML"
        )


@day_router.callback_query(F.data.in_(["dollar", "euro", "yena", "som"]))
async def get_earned_in_valute(
    callback: CallbackQuery, 
    state: FSMContext
) -> None:
    """
    Show the user the data of his earnings 
    in the currency of his choice.
    """
    name: str = callback.data
    text: str = await gen_text(state, name)
    await callback.answer(
        text=text,
        show_alert=True
    )
