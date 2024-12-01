from typing import Dict

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import BOT_TOKEN
from keywords.keyword import cancel_button, menu
from states.two_in_two import TwoInTwo
from utils.two_in_two import two_in_two_get_prediction_sum

two_in_two_router: Router = Router()
bot = Bot(token=BOT_TOKEN)


@two_in_two_router.callback_query(F.data == "two_in_two")
async def two_in_to_get_prediction_scheduler(
        callback: CallbackQuery,
        state: FSMContext
) -> None:
    """Обработчик выбора графика два через два."""
    await state.set_state(TwoInTwo.count_weekday)
    await state.update_data(callback=callback.id)
    await callback.message.answer(
        text="Сколько дополнительных смен вы хотите отработать?",
        reply_markup=cancel_button
    )


@two_in_two_router.message(TwoInTwo.count_weekday, F.text.isdigit())
async def two_in_to_get_prediction_first_day(
        message: Message,
        state: FSMContext
) -> None:
    """Обработчик ввода количества дней подработок."""
    await state.update_data(weekdays=int(message.text))
    await state.set_state(TwoInTwo.first_day)

    await message.answer(
        text="Какого числа ваш первый рабочий день в выбранном месяце?",
        reply_markup=cancel_button
    )


@two_in_two_router.message(TwoInTwo.first_day, F.text.isdigit())
async def two_in_to_get_prediction_first_day(
        message: Message,
        state: FSMContext
) -> None:
    """Обработчик ввода первого дня в месяце."""

    await state.set_state(TwoInTwo.how_many_hours)
    await state.update_data(first_day=int(message.text))
    await message.answer(
        text="Введите количество часов в вашей смене:",
        reply_markup=cancel_button
    )


@two_in_two_router.message(TwoInTwo.how_many_hours, F.text.isdigit())
async def two_in_to_get_prediction_final(
        message: Message,
        state: FSMContext
) -> None:
    """
    Обработчик ввода длительности смены в выбранном месяце. И выводит прогноз
    заработка пользователю.
    """
    await state.update_data(how_many_hours=int(message.text))
    data: Dict[str, int | str] = await state.get_data()
    call_id: str = data.get("callback")
    prediction_sum: tuple = await two_in_two_get_prediction_sum(
        message.from_user.id, data
    )

    if len(prediction_sum) == 1:
        string: str = (f"Ваш прогнозируемый заработок составит "
                       f"{prediction_sum[0]:,.2f}₽")
    else:
        string: str = (f"'Вариант если смены 1, 2'\n"
                       f"Вы заработаете: {prediction_sum[0]:,.2f}₽.\n"
                       f"Вариант если смены 1, 4, 5\nВы заработаете: "
                       f"{prediction_sum[1]:,.2f}₽")

    await bot.answer_callback_query(call_id, string, show_alert=True)
    await message.answer(text="Меню", reply_markup=menu)
