from datetime import datetime as dt, timedelta, datetime, date, UTC
from typing import Tuple, List

import asyncio
from aiogram.types import CallbackQuery

from crud.add_shift import add_many_shifts
from utils.current_day import earned_per_shift
from utils.valute import get_valute_info
from utils.calculate import calc_valute
from keyboards.keyboard import back


async def get_date(action: str) -> Tuple[int, int]:
    """
    Return the month and year for further work with them.

    :param action: The string defining the action.
    :return: A tuple of two integers: (year, month).
    """
    year, month = int(action.split("-")[0]), int(action.split("-")[1])
    return year, month


async def create_data_by_add_shifts(
    user_id: int,
    time: float,
    list_dates: List[str],
    callback: CallbackQuery
) -> None:
    """
    Create shift records for the user based on the provided data.

    :param user_id: The user's ID.
    :param time: The total number of hours worked.
    :param list_dates: A list of string dates in the "YYYY-MM-DD" 
                        format for which You need to create shift records.
    :return: None.
    """
    date_objects = [datetime.strptime(d, "%Y-%m-%d") for d in list_dates]
    sorted_dates = sorted(date_objects)
    
    await callback.answer(text="✅ Начинаем сохранение смен...")
    asyncio.create_task(
        save_shifts_with_progress_bar(user_id, time, sorted_dates, callback)
    )


async def save_shifts_with_progress_bar(
    user_id: int,
    time: float,
    sorted_dates: list,
    callback: CallbackQuery
) -> None:
    """
    Saves with a progress bar.
    
    :param user_id: The user's ID.
    :param time: The number of hours.
    :param sorted_dates: A sorted list of dates.
    :param callback: A callback for displaying a message to the user.
    """
    total = len(sorted_dates)
    try:
        progress_text = create_progress_text(
            0, total, "Начинаем сохранение..."
        )
        await callback.message.edit_text(progress_text)
        
        for i, d in enumerate(sorted_dates, 1):
            date = datetime.strftime(d, "%Y-%m-%d")
            await earned_per_shift(time, user_id, date, {})

            progress_text = create_progress_text(
                i, total, f"Сохранение смены {i}/{total}"
            )
            await callback.message.edit_text(progress_text)
            await asyncio.sleep(0.1)

        success_text = create_progress_text(
            total, total, "✅ Все смены сохранены!"
        )
        await callback.message.edit_text(
            text=success_text,
            reply_markup=back
        )

    except Exception as e:
        error_text = f"❌ Ошибка при сохранении:\n{str(e)}"
        await callback.message.edit_text(error_text)


def create_progress_text(
    current: int,
    total: int,
    status: str
) -> str:
    """
    Create a beautiful progress bar.
    
    :param current: Current progress.
    :param total: Total shifts.
    :param status: Total shifts.
    """
    progress = current / total
    
    if total <= 15:
        bar_length = total
    else:
        bar_length = 15
    
    filled_blocks = int(progress * bar_length)
    empty_blocks = bar_length - filled_blocks
    
    progress_bar = "🟩" * filled_blocks + "⬜" * empty_blocks
    percentage = int(progress * 100)
    
    return (
        f"{status}\n"
        f"{progress_bar} {percentage}%\n"
        f"🎯 {current}/{total} смен сохранено."
    )
