from functools import wraps
from logging.handlers import RotatingFileHandler
from typing import Dict, Callable, ParamSpec, TypeVar
import logging

from aiogram.exceptions import TelegramNetworkError, TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup

from loader import success_text
from utils.current_day import earned_per_shift
from utils.month import create_message
from config import bot
from keyboards.keyboard import back


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
        try:
            logger.info(
                f"\nExecuting function: {func.__name__}\n"
                f"State: {await state.get_data()}"
                f"User ID: {arg.from_user.id}\n"
                f"User: {arg.from_user.full_name} - (@{arg.from_user.username})\n\n"
            )
            await func(arg, state)

        except (KeyError, ValueError) as err:
            logger.error(
                "\nKeyError occurred\n"
                f"Function: {func.__name__}\n"
                f"User ID: {arg.from_user.id}\n"
                f"User: {arg.from_user.full_name} (@{arg.from_user.username}\n",
                exc_info=True,
            )
            await state.clear()
            mess: str = str(err)
            await bot.send_message(arg.from_user.id, mess, reply_markup=back)

        except TelegramNetworkError:
            logger.error(
                "\nTelegramNetworkError\n"
                f"Function: {func.__name__}\n"
                f"User ID: {arg.from_user.id}\n"
                f"User: {arg.from_user.full_name} (@{arg.from_user.username}\n",
                exc_info=True,
            )
            await state.clear()
            mess: str = (
                "У нас проблемы с интернетом, попробуйте зайти чуть позже."
            )
            await bot.send_message(arg.from_user.id, mess, reply_markup=back)

        except TelegramBadRequest:
            logger.error(
                "\nTelegramBadRequest\n"
                f"Function: {func.__name__}\n"
                f"User ID: {arg.from_user.id}\n"
                f"User: {arg.from_user.full_name} (@{arg.from_user.username}\n",
                exc_info=True,
            )
            await state.clear()
            mess: str = (
                "Сбой работы приложения. Попробуйте еще раз."
            )
            await bot.send_message(arg.from_user.id, mess, reply_markup=back)

        # If something unexpected has happened.
        except Exception as e:
            logger.error(
                f"\n{e}\n"
                f"Function: {func.__name__}\n"
                f"User ID: {arg.from_user.id}\n"
                f"User: {arg.from_user.full_name} (@{arg.from_user.username}\n",
                exc_info=True,
            )
            await state.clear()
            mess: str = (
                "Сбой. Попробуйте еще раз."
            )
            await bot.send_message(arg.from_user.id, mess, reply_markup=back)

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
    salary_for_shifts = await earned_per_shift(time, user_id, date, data)
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

