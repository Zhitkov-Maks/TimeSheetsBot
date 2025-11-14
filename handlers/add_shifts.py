from datetime import date
from typing import Dict

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold

from keyboards.add_shifts import get_days_keyboard, days_choices
from keyboards.keyboard import cancel_button, back
from keyboards.add_shifts import prediction_button
from loader import MONTH_DATA
from states.add_shifts import ShiftsState
from utils.add_shifts import get_date, create_data_by_add_shifts
from utils.current_day import valid_time
from utils.decorate import errors_logger

shifts_router: Router = Router()


@shifts_router.message(F.text == "/add")
@errors_logger
async def shifts_calendar(
    message: Message,
    state: FSMContext
) -> None:
    """
    Send the user an inline keyboard to select 
    the days for adding shifts in a group.
    """
    await state.set_state(ShiftsState.hours)
    user_exists = days_choices.get(message.from_user.id)

    if user_exists:
        days_choices.get(message.from_user.id).clear()

    await message.answer(
        text=hbold("Выберите месяц: "),
        reply_markup=await prediction_button(),
        parse_mode="HTML"
    )


@shifts_router.callback_query(ShiftsState.hours)
@errors_logger
async def input_selection_hours(
        callback: CallbackQuery,
        state: FSMContext
) -> None:
    """Ask the user for the number of hours per shift."""
    year, month = await get_date(callback.data)
    current_date: date = date(year, month, 1)

    await state.update_data(
        year=year, month=month, date=str(current_date)
    )

    await state.set_state(ShiftsState.month)
    await callback.message.edit_text(
        text=f"Отлично! Вы выбрали {hbold(MONTH_DATA[month])}. "
             f"\nВведите по сколько часов вам проставить смены?",
        reply_markup=cancel_button,
        parse_mode="HTML"
    )


@shifts_router.message(ShiftsState.month)
@errors_logger
async def work_with_calendar(message: Message, state: FSMContext) -> None:
    """Show the user a calendar for choosing shifts."""
    data: Dict[str, str | float | list] = await state.get_data()
    year, month = int(data["year"]), int(data["month"])
    try:
        time = await valid_time(message.text)
        await state.update_data(time=time)
        await message.answer(
            text="Выберите все смены когда вы работаете.",
            reply_markup=await get_days_keyboard(
                year, month, message.from_user.id)
        )

    except ValueError:
        await message.answer(
            text=hbold("Некорректные данные."),
            reply_markup=cancel_button,
            parse_mode="HTML"
        )


@shifts_router.callback_query(lambda c: c.data.startswith("toggle2_"))
@errors_logger
async def toggle_day(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Add or remove a shift from the collection.
    """
    day: str = callback.data.split("_")[1]
    data: dict = await state.get_data()
    year, month = data["year"], data["month"]
    user_chat_id: int = callback.from_user.id

    if day in days_choices[user_chat_id]:
        days_choices[user_chat_id].remove(day)
        await callback.answer(f"Вы убрали: {day}")

    elif day not in days_choices[user_chat_id]:
        days_choices[user_chat_id].add(day)
        await callback.answer(f"Вы выбрали: {day}")

    await callback.message.edit_reply_markup(
        reply_markup=await get_days_keyboard(year, month, user_chat_id)
    )


@shifts_router.callback_query(F.data == "shift_finish")
@errors_logger
async def finish_add_shifts(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Save the marked days in the database.
    """
    user_id: int = callback.from_user.id
    if len(days_choices.get(user_id)) > 0:
        await state.update_data(user_id=user_id)
        data: Dict[str, str | float] = await state.get_data()
        time = data["time"]

        await create_data_by_add_shifts(
            user_id, time, days_choices[user_id], callback
        )
        days_choices[user_id].clear()

    else:
        await state.clear()
        await callback.message.edit_text(
            text="Вы ничего не выбрали. Нажмине кнопку чтобы открыть календарь.",
            reply_markup=back
        )
