from typing import Dict

from aiogram import Router, Bot
from aiogram import F
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
from utils.current_day import valid_time, earned_for_award
from utils.current_day import gen_message_for_choice_day
from keyboards.current_day import get_data_choices_day

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
async def check_data(message: Message, state: FSMContext) -> None:
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


@create_router.callback_query(F.data == "award")
@decorator_errors
async def add_award(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(CreateState.award)
    await callback.message.answer(
        text=hbold("Введите количество выполненных операция за смену: "),
        reply_markup=cancel_button,
        parse_mode="HTML"
    )


@create_router.message(CreateState.award)
@decorator_errors
async def create_award(message: Message, state: FSMContext) -> None:
    try:
        count_operation: int = int(message.text)
        data: dict = await state.get_data()
        current_id: str = data.get("current_day").get("_id")
        _date, info_for_date = data.get("date"), data.get("current_day")
        update_current_day: dict = await earned_for_award(
            count_operation, message.from_user.id, current_id
        )
        text: str = await gen_message_for_choice_day(
            update_current_day, _date
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
