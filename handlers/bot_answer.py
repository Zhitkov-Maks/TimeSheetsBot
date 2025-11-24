from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from typing import Dict

from utils.current_day import earned_per_shift, get_settings
from utils.month import create_message
from config import bot
from utils.valute import get_valute_info


async def processing_data(
    user_id: int,
    time: float,
    state: FSMContext,
    data: Dict[str, str | int]
) -> None:
    """
    Collect all the necessary data, send it to the database for saving, 
    and send the data for display to the user.

    :param user_id: The user's ID.
    :param time: The total number of hours worked.
    :param state: A state context for managing the user's state in the FSM.
    :param data: A dictionary containing additional data.
    :return: None
    """
    date = data.get("date")
    valute_data: dict[str, tuple[int, float]] = await get_valute_info()
    settings: tuple[float] = await get_settings(user_id)
    day = data.get("current_day")
    notes = data.get("current_day", {}).get("notes")
    
    await earned_per_shift(
        time,
        user_id,
        date,
        notes,
        valute_data=valute_data,
        settings=settings,
        data=data
    )

    callback: str = data.get("callback")
    await send_calendar_and_message(user_id, data, state)


async def send_calendar_and_message(
    user: int,
    data: Dict[str, str],
    state: FSMContext
) -> None:
    """
    Send a message to the user.

    :param user: The ID of the user (chat).
    :param data: A dictionary containing the data needed to generate
                    messages and calendar.
    :param state: A state context for managing the user's state in the FSM.
    :return: None
    """
    calendar: InlineKeyboardMarkup = await create_message(
        user, data["date"], state
    )

    await bot.send_message(
        chat_id=user,
        text="Ваш календарь",
        parse_mode="HTML",
        reply_markup=calendar,
    )
