from typing import Sequence, Tuple

from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup

from crud.statistics import get_information_for_month
from states.state import MonthState
from utils.gen_message_period import create_calendar, generate_str


async def create_message(
    user_id: int, date: str, state: FSMContext
) -> Tuple[str, InlineKeyboardMarkup]:
    """
    Функция собирает информацию для отображения календаря и сообщения о зарплате.
    :param user_id: ID пользователя.
    :param date: Переданная дата
    :param state: Состояние.
    :return: Сообщение и календарь.
    """
    year: int = int(date[:4])
    month: int = int(date[5:7])
    await state.clear()
    await state.set_state(MonthState.choice)
    await state.update_data(year=year, month=month)

    result: Sequence = await get_information_for_month(user_id, year, month)
    calendar: InlineKeyboardMarkup = await create_calendar(result, year, month)

    message: str = await generate_str(result, month)

    return message, calendar
