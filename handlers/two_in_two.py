from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold

from keywords.keyword import cancel_button, menu
from states.Prediction import TwoInTwo
from utils.prediction import two_in_two_get_prediction_sum

two_in_two_router = Router()


@two_in_two_router.callback_query(F.data == "two_in_two")
async def two_in_to_get_prediction_scheduler(callback: CallbackQuery,
                                             state: FSMContext) -> None:
    """Обработчик выбора графика 2 через два."""
    await state.set_state(TwoInTwo.weekday)
    await callback.message.answer(
        text="Сколько дополнительных смен вы хотите отработать.",
        reply_markup=cancel_button
    )


@two_in_two_router.message(TwoInTwo.weekday, F.text.isdigit())
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
        text="Сколько часов считать в вашей смене(Обычно два через два "
             "подразумевает смены по 12 часов, но иногда работодатели считают по 11 "
             "часов, так как час отводится на обед.)",
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
    data: dict = await state.get_data()
    prediction_sum: tuple = await two_in_two_get_prediction_sum(message.from_user.id,
                                                         data)
    if len(prediction_sum) == 1:
        string: str = f"Ваш прогнозируемый заработок составит {prediction_sum[0]:,.2f}₽"
    else:
        string: str = (f"Вы указали что первый рабочий день "
                       f"первого числа. Здесь может быть два "
                       f"варианта. \n"
                       f"{hbold("Первый")} вы работаете 1 и 2 "
                       f"числа и ваш заработок составит - {prediction_sum[0]:,.2f}₽.\n"
                       f"{hbold("Второй")} вариант вы работаете первого, "
                       f"а второго не работаете и тогда ваш "
                       f"заработок составит - "
                       f" {prediction_sum[1]:,.2f}₽")

    await message.answer(
            text=string,
            parse_mode="HTML",
            reply_markup=await menu()
        )
