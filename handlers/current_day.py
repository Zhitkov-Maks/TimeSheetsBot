from typing import Dict

from aiogram import Router, Bot
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold

from config import BOT_TOKEN
from crud.create import delete_record
from handlers.bot_answer import send_calendar_and_message, processing_data, \
    decorator_errors
from keyboards.keyboard import cancel_button, menu
from loader import add_record_text
from states.current_day import CreateState
from utils.current_day import valid_time

create_router = Router()
bot = Bot(token=BOT_TOKEN)


@create_router.callback_query(F.data.in_(["change", "add"]))
@decorator_errors
async def on_date_today(callback: CallbackQuery, state: FSMContext) -> None:
    """Обработчик команд для добавления или изменения записи о смене."""
    await state.update_data(action=callback.data, callback=callback.id)
    await state.set_state(CreateState.check_data)
    await callback.message.edit_text(
        text=add_record_text, reply_markup=cancel_button
    )


@create_router.message(CreateState.check_data)
@decorator_errors
async def check_data(message: types.Message, state: FSMContext) -> None:
    """
    Сохранение и проверка введенного отработанного времени. Если проверка
    проходит, то отправляем на расчет заработка и добавление записи в бд.
    А затем заново открывает календарь.
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
            "Введенные данные не соответствуют требованиям. \n"
            "Пример: 6.5. Попробуйте еще раз.",
            reply_markup=cancel_button,
        )

    except KeyError as err:
        await message.answer(
            text=hbold(str(err)),
            reply_markup=menu,
            parse_mode="HTML"
        )


@create_router.callback_query(F.data == "del")
@decorator_errors
async def del_record(callback: CallbackQuery, state: FSMContext) -> None:
    """Отправка на удаление записи."""
    await state.update_data(user_id=callback.from_user.id)
    data: Dict[str, str] = await state.get_data()

    await delete_record(data.get("date"), callback.from_user.id)
    await callback.answer("Запись удалена!!!")
    await send_calendar_and_message(callback.from_user.id, data, state)
