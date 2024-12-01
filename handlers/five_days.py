from typing import List

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold

from keywords.keyword import cancel_button
from keywords.prediction import get_weekdays_keyboard, user_choices, \
    hour_choices, choices_days
from states.five_days import FiveState
from utils.five_days import get_prediction_sum

five_days_router: Router = Router()


@five_days_router.callback_query(F.data == "five_days")
async def five_days_get_prediction_scheduler(
        callback: CallbackQuery, state: FSMContext
) -> None:
    """Обработчик команды для прогнозирования заработка пятидневки."""
    await state.set_state(FiveState.weekday)
    await callback.message.answer(
        text="Сколько дополнительных смен вы хотите отработать.",
        reply_markup=cancel_button
    )


@five_days_router.message(FiveState.weekday)
async def five_days_how_many_hours(
        message: Message,
        state: FSMContext
) -> None:
    await state.set_state(FiveState.how_many_hours)
    await state.update_data(weekdays=int(message.text))
    await message.answer(
        text="По сколько часов ставится смена?",
        reply_markup=cancel_button
    )


@five_days_router.message(FiveState.how_many_hours, F.text.isdigit())
async def five_days_get_prediction_delay(
        message: Message,
        state: FSMContext
) -> None:
    """
    Обрабатывает количество доп смен. Показывает инлайн клавиатуру, которая
    имитирует работу checkbox.
    """
    await state.update_data(how_many_hours=int(message.text))
    await state.set_state(FiveState.checkbox)

    await message.answer(
        text=f"Если вы задерживаетесь после основной смены, то выберите по "
             f"каким дням, и по сколько часов. Дни можно выбрать все. Часы должен "
             f"быть только выбран {hbold("один")} вариант иначе будет считаться "
             f"по минимальному.",
        parse_mode="HTML",
        reply_markup=await get_weekdays_keyboard()
    )


@five_days_router.callback_query(lambda c: c.data.startswith("toggle_"))
async def toggle_day(callback_query: CallbackQuery) -> None:
    """
    Обработчик выбора вариантов рабочих дней и количества доп часов.
    """
    day: str = callback_query.data.split("_")[1]

    # Обновляем состояние выбора
    if not day.isdigit() and day in user_choices:
        user_choices.remove(day)
        await callback_query.answer(f"Вы убрали: {day}")

    elif not day.isdigit() and day not in user_choices:
        user_choices.append(day)
        await callback_query.answer(f"Вы выбрали: {day}")

    elif day.isdigit() and day in hour_choices:
        hour_choices.remove(day)
        await callback_query.answer(f"Вы убрали: {day} часа дополнительно.")

    elif day.isdigit() and day not in hour_choices:
        hour_choices.append(day)
        await callback_query.answer(f"Вы выбрали: {day} часа дополнительно.")

    await callback_query.message.edit_reply_markup(
        reply_markup=await get_weekdays_keyboard())


@five_days_router.callback_query(F.data == "finish")
async def finish_selection(
        callback_query: CallbackQuery, state: FSMContext
) -> None:
    delay_list: List[int] = []

    if user_choices:
        for i in user_choices:
            delay_list.append(choices_days.get(i))
        await state.update_data(delay=delay_list)

    else:
        await state.update_data(delay="delay_no")

    if hour_choices:
        await state.update_data(hour=hour_choices[0])
    else:
        await state.update_data(hour=3)

    data: dict = await state.get_data()
    prediction_sum: int = await get_prediction_sum(
        callback_query.from_user.id, data
    )
    await callback_query.answer(
        text=f"Ваш прогнозируемый заработок составит: {prediction_sum:,.2f}₽",
        show_alert=True
    )
    user_choices.clear()
    hour_choices.clear()
