from datetime import date
from typing import List, Dict

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold

from config import BOT_TOKEN
from handlers.bot_answer import send_calendar_and_message, decorator_errors
from keywords.add_shifts import get_days_keyboard, days_choices
from keywords.keyword import cancel_button, menu
from keywords.prediction import prediction_button
from loader import MONTH_DATA
from states.add_shifts import ShiftsState
from utils.add_shifts import get_date, create_data_by_add_shifts
from utils.current_day import split_data

shifts_router: Router = Router()
bot: Bot = Bot(token=BOT_TOKEN)


@shifts_router.callback_query(F.data == "many_add")
@decorator_errors
async def shifts_calendar(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик команды для групповой отметки смен. Отправляет пользователю
    инлайн клавиатуру для выбора месяца.
    """
    await state.set_state(ShiftsState.hours)
    await callback.message.answer(
        text="За какой месяц будем проставлять смены?",
        reply_markup=await prediction_button()
    )


@shifts_router.callback_query(
    ShiftsState.hours,
    F.data.in_(["current", "next_month"]))
@decorator_errors
async def input_selection_hours(
        callback: CallbackQuery,
        state: FSMContext
) -> None:
    """
    Обработчик обрабатывает выбранный месяц. И запрашивает у пользователя по
    сколько часов проставить смены.
    """
    year, month = await get_date(callback.data)
    current_date: date = date(year, month, 1)

    await state.update_data(
        year=year, month=month, date=str(current_date)
    )

    await state.set_state(ShiftsState.month)
    await callback.message.answer(
        text=f"Отлично! Вы выбрали {hbold(MONTH_DATA[month])}. "
             f"\nВведите по сколько часов вам проставить смены?",
        reply_markup=cancel_button
    )


@shifts_router.message(ShiftsState.month)
@decorator_errors
async def work_with_calendar(message: Message, state: FSMContext) -> None:
    """
    Обработчик введенных часов, получает число в зависимости от
    пользовательского ввода. Показывает пользователю календарь за выбранный
    месяц, чтобы выбрать дни для добавления смен.
    """
    data: Dict[str, str | float | list] = await state.get_data()
    year, month = int(data["year"]), int(data["month"])
    numbers: List[str] = message.text.split("*")
    try:
        if len(numbers) == 1 or len(numbers) == 2:
            time, overtime = await split_data(numbers)
            await state.update_data(time=time, overtime=overtime)
        else:
            raise ValueError

    except ValueError:
        await message.answer(
            "Введенные данные не соответствуют требованиям. \n"
            "Пример: 6.5*5. Попробуйте еще раз.",
            reply_markup=cancel_button,
        )
    await message.answer(
        text=f"Выберите все смены когда вы работаете.",
        reply_markup=await get_days_keyboard(year, month, message.from_user.id)
    )


@shifts_router.callback_query(lambda c: c.data.startswith("toggle2_"))
@decorator_errors
async def toggle_day(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик выбранных дней. Добавляет или убирает дни в словарь, где ключ
    идентификатор пользователя, значение множество выбранных дней.
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
@decorator_errors
async def finish_add_shifts(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик выбранных дней, отправляет запрос на добавление смен в бд.
    """
    user_id: int = callback.from_user.id
    if days_choices[user_id]:
        await state.update_data(user_id=user_id)
        data: Dict[str, str | float] = await state.get_data()
        time, overtime = data["time"], data["overtime"]

        await create_data_by_add_shifts(
            user_id, time, overtime, days_choices[user_id]
        )
        await callback.answer("Записи были успешно добавлены!")
        await send_calendar_and_message(user_id, data, state)

    else:
        await state.clear()
        await callback.message.answer(
            text="Вы ничего не выбрали, открываю вам меню!",
            reply_markup=menu
        )
