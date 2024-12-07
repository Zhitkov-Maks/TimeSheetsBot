from aiogram.types import User

from logger_config import bot_logger


async def write_logger_error(exc: str, user: User, func_name: str) -> None:
    """
    Функция записывает сообщение в файл.
    :param exc: Исключение, которое вышло при ошибке.
    :param user: Пользователь телеграм.
    :param func_name: Имя функции в которой произошла ошибка.
    """
    bot_logger.info(user)
    bot_logger.error(
        f"User: {user.username}, "
        f"Исключение: '{exc}', "
        f"function: '{func_name}'"
    )
