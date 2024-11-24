import asyncio
from typing import List, Dict

from aiogram import Router, Bot
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import BOT_TOKEN
from crud.create import delete_record
from handlers.bot_answer import send_calendar_and_message, processing_data, \
    delete_message_after_delay
from keywords.keyword import cancel_button
from loader import add_record_text
from states.state import CreateState

create_router = Router()
bot = Bot(token=BOT_TOKEN)


@create_router.callback_query(F.data.in_(["change", "add"]))
async def on_date_today(callback: CallbackQuery, state: FSMContext) -> None:
    """Обработчик команд для добавления или изменения записи о смене."""
    await state.update_data(action=callback.data)
    await state.set_state(CreateState.check_data)
    send_message: Message = await callback.message.answer(text=add_record_text,
                                                          reply_markup=cancel_button)

    await asyncio.create_task(delete_message_after_delay(callback.message, 0))
    await asyncio.create_task(delete_message_after_delay(send_message, 15))


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

            if len(numbers) == 1:
                time, overtime = float(numbers[0]), 0

            else:
                time, overtime = float(numbers[0]), float(numbers[1])

            if time + overtime > 24 or time > 24 or time + overtime < 1:
                raise ValueError

            await processing_data(
                message.from_user.id, time, overtime, state, data
            )

        else:
            raise ValueError

    except ValueError:
        await message.answer(
            "Введенные данные не соответствуют требованиям. \n"
            "Пример: 6.5*5. Попробуйте еще раз.",
            reply_markup=cancel_button,
        )
    asyncio.create_task(delete_message_after_delay(message, 0))


@create_router.callback_query(F.data == "del")
async def zero_record(callback: CallbackQuery, state: FSMContext) -> None:
    """Отправка на удаление записи."""
    await state.update_data(user_id=callback.from_user.id)
    data: Dict[str, str] = await state.get_data()

    await delete_record(data)
    send_message: Message = await callback.message.answer(
        text="Запись была удалена.",
        parse_mode="HTML",
    )
    await send_calendar_and_message(callback.from_user.id, data, state)
    await asyncio.create_task(delete_message_after_delay(callback.message, 0))
    await asyncio.create_task(delete_message_after_delay(send_message, 10))
