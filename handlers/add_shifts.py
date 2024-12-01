from datetime import date
from typing import List, Dict

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import BOT_TOKEN
from handlers.bot_answer import send_calendar_and_message
from keywords.add_shifts import get_days_keyboard, days_choices
from keywords.keyword import cancel_button, menu
from keywords.prediction import prediction
from states.add_shifts import ShiftsState
from utils.add_shifts import get_date, create_data_by_add_shifts
from utils.current_day import split_data

shifts_router: Router = Router()
bot = Bot(token=BOT_TOKEN)


@shifts_router.callback_query(F.data == "many_add")
async def shifts_calendar(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(ShiftsState.month)
    await callback.message.answer(
        text="Выберите месяц для отметки смен.",
        reply_markup=await prediction()
    )


@shifts_router.callback_query(
    ShiftsState.month, F.data.in_(["current", "next_month"]))
async def work_with_calendar(
        callback: CallbackQuery,
        state: FSMContext
) -> None:
    year, month = await get_date(callback.data)
    current_date: date = date(year, month, 1)
    await state.update_data(
        year=year, month=month, date=str(current_date))
    await callback.message.answer(
        text="Отметьте все смены когда вы работаете.",
        reply_markup=await get_days_keyboard(year, month)
    )


@shifts_router.callback_query(lambda c: c.data.startswith("toggle2_"))
async def toggle_day(
        callback_query: CallbackQuery,
        state: FSMContext
) -> None:
    day: str = callback_query.data.split("_")[1]
    data = await state.get_data()
    year, month = data["year"], data["month"]
    if day in days_choices:
        days_choices.remove(day)
        await callback_query.answer(f"Вы убрали: {day}")

    elif day not in days_choices:
        days_choices.append(day)
        await callback_query.answer(f"Вы выбрали: {day}")

    await callback_query.message.edit_reply_markup(
        reply_markup=await get_days_keyboard(year, month)
    )


@shifts_router.callback_query(F.data == "shift_finish")
async def input_selection_hours(
        callback_query: CallbackQuery,
        state: FSMContext
) -> None:
    if days_choices:
        await state.set_state(ShiftsState.hours)
        await state.update_data(days=days_choices, call=callback_query.id)
        await callback_query.message.answer(
            text="Введите по сколько часов вам проставить смены?",
            reply_markup=cancel_button
        )

    else:
        await state.clear()
        await callback_query.message.answer(
            text="Вы ничего не выбрали, открываю вам меню!",
            reply_markup=menu
        )


@shifts_router.message(ShiftsState.hours)
async def finish_add_shifts(
        message: Message,
        state: FSMContext
) -> None:
    """
    Функция для завершения проставления смен.
    """
    await state.update_data(user_id=message.from_user.id)
    data: Dict[str, str | float | list] = await state.get_data()
    call_id: str = data.get("call")

    numbers: List[str] = message.text.split("*")
    try:
        if len(numbers) == 1 or len(numbers) == 2:
            time, overtime = await split_data(numbers)

            await create_data_by_add_shifts(
                message.from_user.id, time, overtime, data.get("days")
            )
            await bot.answer_callback_query(
                call_id, "Записи были успешно добавлены!", cache_time=60
            )
            await send_calendar_and_message(message.from_user.id, data, state)
        else:
            raise ValueError

    except ValueError:
        await message.answer(
            "Введенные данные не соответствуют требованиям. \n"
            "Пример: 6.5*5. Попробуйте еще раз.",
            reply_markup=cancel_button,
        )
    except TelegramBadRequest:
        await message.answer(
            text="Время ожидания истекло, попробуйте еще раз!"
        )
    days_choices.clear()
