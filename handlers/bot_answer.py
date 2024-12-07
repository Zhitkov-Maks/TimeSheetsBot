from functools import wraps
from typing import Dict, Callable, ParamSpec, TypeVar

from aiogram import Bot
from aiogram.exceptions import TelegramNetworkError, TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup

from config import BOT_TOKEN
from crud.create import write_salary, update_salary
from loader import success_text
from utils.current_day import earned_salary
from utils.month import create_message

bot = Bot(token=BOT_TOKEN)


T = TypeVar("T")
P = ParamSpec("P")


def decorator_errors(func: Callable[P, T]) -> Callable[P, T]:
    """
    Декоратор для функции обработки колбеков и сообщений.
    """
    @wraps(func)
    async def wrapper(arg: P, state: FSMContext) -> None:
        """
        Обертка для обработки ошибок при выполнении функции.
        """
        try:
            return await func(arg, state)

        except KeyError:
            mess: str = (
                "I'm Sorry! Произошла ошибка при обработке данных."
                " Возможные причина ошибки - вы нажали кнопку, "
                "которая с течением времени уже не содержит "
                "никаких данных."
            )
            await bot.send_message(arg.from_user.id, mess)
        except TelegramNetworkError:
            mess: str = (
                "У нас проблемы с интернетом, попробуйте зайти чуть позже."
            )
            await bot.send_message(arg.from_user.id, mess)
        except TelegramBadRequest:
            mess: str = (
                "Что-то сломалось. Ошибка на нашей стороне, пришлите мне подробно"
                "какие действия вы совершали."
            )
            await bot.send_message(arg.from_user.id, mess)

    return wrapper


@decorator_errors
async def processing_data(
        user_id: int,
        time: float,
        overtime: float,
        state: FSMContext,
        data: Dict[str, str | int]
) -> None:
    """
    Обрабатывает данные о зарплате пользователя, вычисляет заработок и обновляет
    записи в базе данных.

    Эта функция выполняет следующие действия:
    1. Вычисляет базовую зарплату, сверхурочные и общую заработанную сумму.
    2. Отправляет пользователю сообщение с информацией о заработке.
    3. В зависимости от действия (добавить или обновить) записывает или
        обновляет данные о зарплате в базе данных.
    4. Отправляет календарь и соответствующее сообщение пользователю.

    :param user_id: Идентификатор пользователя (чата), которому будет
                    отправлено сообщение.
    :param time: Общее количество отработанных часов.
    :param overtime: Количество сверхурочных часов.
    :param state: Контекст состояния для управления состоянием пользователя
                    в FSM.
    :param data: Словарь, содержащий дополнительные данные, такие как
                дата и действие (например, "add" или "update").

    :return: None
    """
    base, overtime, earned = await earned_salary(time, overtime, user_id)
    callback: str = data.get("callback")
    await bot.answer_callback_query(
        callback_query_id=callback,
        text=success_text.format(data["date"], earned),
        show_alert=True
    )

    if data["action"] == "add":
        await write_salary(base, overtime, earned, data)

    else:
        await update_salary(base, overtime, earned, data)
    await send_calendar_and_message(user_id, data, state)


@decorator_errors
async def send_calendar_and_message(
        user: int,
        data: Dict[str, str],
        state: FSMContext
) -> None:
    """
    Отправляет пользователю текущий календарь после добавления записи за
    выбранный день.
    Эта функция генерирует сообщение и инлайн-клавиатуру с календарем на основе
    переданных данных, а затем отправляет их пользователю.

    :param user: Идентификатор пользователя (чата), которому будет отправлено
                    сообщение.
    :param data: Словарь, содержащий данные, необходимые для генерации
                    сообщения и календаря. Ожидается наличие ключа "date",
                    который представляет собой дату записи.
    :param state: Контекст состояния для управления состоянием пользователя
                    в FSM (Finite State Machine).

    :return: None
    """
    calendar: InlineKeyboardMarkup = await create_message(
        user, data["date"], state
    )

    await bot.send_message(
        chat_id=user,
        text="...",
        parse_mode="HTML",
        reply_markup=calendar,
    )
