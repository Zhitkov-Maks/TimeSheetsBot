from functools import wraps
from logging.handlers import RotatingFileHandler
from typing import Dict, Callable, ParamSpec, TypeVar
import logging
from datetime import datetime

from aiogram.exceptions import TelegramNetworkError, TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.markdown import hbold

from keyboards.month import create_calendar
from loader import success_text
from utils.month import get_data_for_calendar
from utils.current_day import earned_per_shift, get_settings
from utils.month import create_message
from config import bot
from utils.valute import get_valute_info


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    filename="/salary/logs/time_bot.log",
    maxBytes=10 * 1024 * 1024,
    backupCount=10,
    encoding="utf-8",
)

handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)

# Adding a handler to the logger
logger.addHandler(handler)


T = TypeVar("T")
P = ParamSpec("P")


def decorator_errors(func: Callable[P, T]) -> Callable[P, T]:
    """
    A decorator for callback and message processing functions.
    """
    @wraps(func)
    async def wrapper(arg: P, state: FSMContext) -> None:
        """
        Handle possible errors when using the bot. 
        And write them to a file.
        """
        success = False
        error_type = None
        error_message = None

        try:
            logger.info(
                f"\nSTART: {func.__name__}\n"
                f"User ID: {arg.from_user.id}\n"
                f"State: {await state.get_data()}\n"
            )
            await func(arg, state)
            success = True

        except (KeyError, ValueError) as err:
            error_type = "KeyError/ValueError"
            error_message = str(err)
            await state.clear()

        except TelegramNetworkError as err:
            error_type = "TelegramNetworkError"
            error_message = str(err)
            await state.clear()

        except TelegramBadRequest as err:
            error_type = "TelegramBadRequest"
            error_message = str(err)
            await state.clear()

        except Exception as err:
            error_type = "UnexpectedError"
            error_message = str(err)
            await state.clear()

        finally:
            if success:
                logger.info(
                    f"\nSUCCESS: {func.__name__}\n"
                    f"User ID: {arg.from_user.id}\n"
                )
            else:
                logger.error(
                    f"\nFAILED: {func.__name__}\n"
                    f"User ID: {arg.from_user.id}\n"
                    f"Error Type: {error_type}\n"
                    f"Error: {error_message}\n",
                    exc_info=not isinstance(
                        error_message, (KeyError, ValueError)
                    )  # exc_info только для неожиданных ошибок
                )

                year: int = datetime.now().year
                month: int = datetime.now().month

                result, data = await get_data_for_calendar(
                    arg.from_user.id, year, month, state
                )

                await bot.send_message(
                    arg.from_user.id,
                    text=hbold("Ошибка обработки данных. Попробуйте еще раз."), 
                    reply_markup=await create_calendar(
                        result, year, month, data
                    ),
                    parse_mode="HTML"
                )
    return wrapper


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

    salary_for_shifts = await earned_per_shift(
        time,
        user_id,
        date,
        data,
        valute_data=valute_data,
        settings=settings
    )

    callback: str = data.get("callback")
    await bot.answer_callback_query(
        callback_query_id=callback,
        text=success_text.format(data["date"], salary_for_shifts),
        show_alert=True
    )
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
