import re
import datetime

from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup
from aiogram import Router
from aiogram import types, F
from aiogram.utils.markdown import hbold

from aiogram_calendar import (
    DialogCalendar,
    DialogCalendarCallback
)

from config import menu
from crud.create import write_salary, check_record_salary, update_salary, \
    delete_record
from database.models import Salary
from loader import select_keyboard, add_record_text, success_text, \
    reset_to_zero
from states.state import CreateState
from utils.count import earned_salary

create_router = Router()


@create_router.callback_query(F.data == "select_date")
async def on_date_selected(callback: CallbackQuery) -> None:
    """Обработчик команды select_date. Запускает календарь."""
    await callback.message.answer(
        text="Выберите дату",
        reply_markup=await DialogCalendar().start_calendar()
    )


@create_router.callback_query(F.data == "today")
async def on_date_today(
        callback: CallbackQuery, state: FSMContext
) -> None:
    """
    Обработчик команды today, чтобы быстрее
    добавить запись по текущему дню.
    """
    date = datetime.datetime.now()
    await state.update_data(date=date.strftime("%d/%m/%Y"))
    await state.set_state(CreateState.select_date)
    await callback.message.answer(text=add_record_text)


@create_router.callback_query(DialogCalendarCallback.filter())
async def process_simple_calendar(
        callback_query: CallbackQuery,
        callback_data: CallbackData,
        state: FSMContext
) -> None:
    """Обрабатывает выбранную дату."""
    selected, select_date = await DialogCalendar().process_selection(
        callback_query, callback_data
    )
    if selected:
        await state.update_data(date=select_date.strftime("%d/%m/%Y"))
        await state.set_state(CreateState.select_date)
        await callback_query.message.answer(text=add_record_text)


@create_router.message(CreateState.select_date)
async def ask_count_hours(
        message: types.Message, state: FSMContext
) -> None:
    await state.update_data(user_id=message.from_user.id)
    data: dict = await state.get_data()
    check_record: Salary = await check_record_salary(
        message.from_user.id, data["date"]
    )
    num_list = re.findall(r'\b\d+\b', message.text)
    if check_record is None:
        base, overtime, earned = await earned_salary(
            num_list, message.from_user.id
        )

        await state.update_data(earned=earned)
        await write_salary(base, overtime, earned, data)

        await message.answer(
            text=success_text.format(data["date"], hbold(earned)),
            parse_mode="HTML",
            reply_markup=menu
        )

    else:
        keyword = ReplyKeyboardMarkup(
            keyboard=select_keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await state.set_state(CreateState.confirm)
        await state.update_data(num_list=num_list)
        await message.answer(
            text=f"В дате {data["date"]} уже есть данные\n"
                 f"-------------------------------------------------------\n"
                 f"База: {check_record.base_hours}\n"
                 f"Доп часы: {check_record.overtime}\n"
                 f"Итого заработано: {check_record.earned}\n"
                 f"--------------------------------------------------------\n"
                 f"Хотите обновить данные?",
            reply_markup=keyword
        )


@create_router.message(
    (F.text.lower() == "да") | (F.text.lower() == "нет"),
    CreateState.confirm
)
async def confirm_update_record(
        message: types.Message, state: FSMContext
) -> None:
    """Функция на обработку обновить данные или нет."""
    if message.text.lower() == "нет":
        await state.clear()
        await message.answer(
            text="Ок направляю вас в меню",
            reply_markup=menu
        )

    else:
        data = await state.get_data()
        if len(data["num_list"]) == 1 and int(data["num_list"][0]) == 0:
            await state.set_state(CreateState.zero)
            keyword = ReplyKeyboardMarkup(
                keyboard=reset_to_zero,
                resize_keyboard=True,
                one_time_keyboard=True
            )
            await message.answer(
                text="Вы хотите удалить запись?",
                reply_markup=keyword
            )
        else:
            base, overtime, earned = await earned_salary(
                data["num_list"], message.from_user.id
            )

            await state.update_data(earned=earned)
            await update_salary(base, overtime, earned, data)
            await message.answer(
                text=success_text.format(data["date"], hbold(earned)),
                parse_mode="HTML",
                reply_markup=menu
            )


@create_router.message(
    (F.text.lower() == "да") | (F.text.lower() == "нет"),
    CreateState.zero
)
async def zero_record(message: types.Message, state: FSMContext) -> None:
    """Отправка на удаление записи."""
    if message.text.lower() == "нет":
        await message.answer(
            text="Ок, возвращаю вас в меню.",
            reply_markup=menu
        )
    else:
        data = await state.get_data()
        await delete_record(data)
        await message.answer(
            text="Запись была удалена.",
            reply_markup=menu
        )