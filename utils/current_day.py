"""Вспомогательный модуль для подсчета зарплаты за выбранный день."""
from aiogram.utils.markdown import hbold
from dataclasses import dataclass
from typing_extensions import Tuple

from crud.settings import get_settings_user_by_id
from database import Settings
from database.models import Salary


@dataclass
class Employee:
    """
    Класс нужен если пользователь, не сделал настройки под себя,
    тогда делаем значение по умолчанию.
    """
    price: float
    overtime: float


async def earned_per_shift(base: float, overtime: float, user_id: int) -> float:
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
    earned: float = await earned_per_shift(time, overtime, user_id)
    return time, overtime, earned


async def gen_message_for_choice_day(salary: Salary, choice_date: str) -> str:
    """
    Генерируем простое сообщения по з/п за выбранную смену для пользователя.

    :param choice_date: Переданная дата из календаря.
    :param salary: Заработок за определенный день.
    :return: Сообщение для пользователя.
    """
    if not salary:
        return f"За дату {choice_date} нет данных."

    other: float = salary.other_income if salary.other_income else 0
    return (
        f"Дата: {choice_date}. \nВы отработали: "
        f"{hbold(salary.base_hours + salary.overtime)} часов.\n"
        f"Заработали: {salary.earned + other:,.2f}₽.\n"
        f"Из них прочие доходы: {other:,.2f}₽."
    )
