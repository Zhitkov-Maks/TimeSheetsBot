"""Вспомогательный модуль для подсчета зарплаты за выбранный день."""

from typing_extensions import Tuple

from crud.settings import get_settings_user_by_id
from database import Settings


class Employee:
    """
    Класс нужен если пользователь, не сделал настройки под себя,
    тогда делаем значение по умолчанию.
    """

    def __init__(self, price, overtime):
        self.price = price
        self.overtime = overtime


async def earned_per_shift(base: float, overtime: float, user_id: int) -> int:
    """
    Формируем сумму, заработанную за смену.
    :param base: Базовая ставка.
    :param overtime: Доплата за переработку.
    :param user_id: Id юзера.
    :return: Заработанную сумму за месяц.
    """
    settings: Settings | Employee = await get_settings_user_by_id(user_id)
    if settings is None:
        settings = Employee(300, 100)
    return round(
        base * settings.price + overtime * (settings.price + settings.overtime), 2
    )


async def earned_salary(
    time: float, overtime: float, user_id: int
) -> Tuple[float, float, float]:
    """
    Промежуточная функция, для получения нужных нам данных
    для вывода сообщения.
    :param time: Отработанное время.
    :param overtime: Переработано.
    :param user_id: Id пользователя.
    :return: Кортеж с временем, переработкой, заработком.
    """
    earned: int = await earned_per_shift(time, overtime, user_id)
    return time, overtime, earned
