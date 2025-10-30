from functools import wraps
from logging.handlers import RotatingFileHandler
from typing import Dict, Callable, ParamSpec, TypeVar
import logging

from aiogram.exceptions import TelegramNetworkError, TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup

from loader import success_text
from utils.current_day import earned_salary
from utils.month import create_message
from crud.create import write_salary
from config import bot
from keyboards.keyboard import menu


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

# Добавляем обработчик к логгеру
logger.addHandler(handler)


T = TypeVar("T")
P = ParamSpec("P")


def decorator_errors(func: Callable[P, T]) -> Callable[P, T]:
    """
    Декоратор для функции обработки колбэков и сообщений.
    """
    @wraps(func)
    async def wrapper(arg: P, state: FSMContext) -> None:
        """
        Обертка для обработки ошибок при выполнении функции.
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
            await bot.send_message(arg.from_user.id, mess, reply_markup=menu)

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
            await bot.send_message(arg.from_user.id, mess, reply_markup=menu)

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
                "Что-то сломалось. Ошибка на нашей стороне, пришлите мне "
                "подробно какие действия вы совершали."
            )
            await bot.send_message(arg.from_user.id, mess, reply_markup=menu)

        # Если произошло что-то неожиданное.
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
            await bot.send_message(arg.from_user.id, mess, reply_markup=menu)

    return wrapper


async def processing_data(
        user_id: int,
        time: float,
        state: FSMContext,
        data: Dict[str, str | int]
) -> None:
    """
    Обрабатывает данные о зарплате пользователя, вычисляет заработок
    и обновляет записи в базе данных.

    :param user_id: Идентификатор пользователя.
    :param time: Общее количество отработанных часов.
    :param state: Контекст состояния для управления состоянием пользователя
                    в FSM.
    :param data: Словарь, содержащий дополнительные данные.
    :return: None
    """
    base, earned_hours, earned_cold = await earned_salary(time, user_id)
    callback: str = data.get("callback")
    await bot.answer_callback_query(
        callback_query_id=callback,
        text=success_text.format(data["date"], earned_hours + earned_cold),
        show_alert=True
    )

    await write_salary(base, earned_hours, earned_cold, data)
    await send_calendar_and_message(user_id, data, state)


async def send_calendar_and_message(
        user: int,
        data: Dict[str, str],
        state: FSMContext
) -> None:
    """
    Отправляет пользователю текущий календарь после добавления записи за
    выбранный день.

    :param user: Идентификатор пользователя (чата).
    :param data: Словарь, содержащий данные, необходимые для генерации
                    сообщения и календаря..
    :param state: Контекст состояния для управления состоянием пользователя
                    в FSM (Finite State Machine).
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
