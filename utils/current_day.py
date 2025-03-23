"""Вспомогательный модуль для подсчета зарплаты за выбранный день."""

from loader import MONTH_DATA, money
from crud.settings import get_settings_user_by_id


async def earned_per_shift(base: float, user_id: int) -> tuple[float, float]:
    """
    Формируем сумму, заработанную за смену.

    :param base: Базовая ставка.
    :param overtime: Доплата за переработку.
    :param user_id: Id юзера.
    :return: Заработанную сумму за месяц.
    """
    settings: dict = await get_settings_user_by_id(user_id)
    if not settings:
        raise KeyError(
            "Чтобы добавить запись необходимо указать ваши параметры"
            " для расчета в настройках."
            )

    price: float = settings.get("price_time", 0)
    cold: float = settings.get("price_cold", 0)

    earned_hours: float = round(base * float(price), 2)
    earned_cold: float = round(base * float(cold), 2)
    return earned_hours, earned_cold


async def earned_salary(time: float, user_id: int) -> tuple:
    """
    Промежуточная функция, для получения нужных нам данных
    для вывода сообщения.
    :param time: Отработанное время.
    :param overtime: Переработано.
    :param user_id: Id пользователя.
    :return: Кортеж с временем, переработкой, заработком.
    """
    earned_hours, earned_cold = await earned_per_shift(time, user_id)
    return time, earned_hours, earned_cold


async def gen_message_for_choice_day(salary: dict, choice_date: str) -> str:
    """
    Генерируем простое сообщения по з/п за выбранную смену для пользователя.

    :param choice_date: Переданная дата из календаря.
    :param salary: Заработок за определенный день.
    :return: Сообщение для пользователя.
    """
    month, day = int(choice_date[5:7]), choice_date[8:]
    day_month: str = f"{MONTH_DATA[month]} {day}"
    if not salary:
        return f"{day_month}, нет данных."
    
    detail_message: str = ""
    if salary.get("earned_cold"):
        detail_message += f"""Оплата часов: {salary.get("earned_hours")}{money}.
Доплата за холод: {salary.get("earned_cold")}{money}.
    """

    return f"""
Информация за {MONTH_DATA[month]} {day}.
--------------------------------------------
Отработано часов: {salary.get("base_hours")}ч.
Заработано: {salary.get("earned")}{money}.
{detail_message}
    """


async def valid_time(time: str) -> float:
    """
    Небольшая проверка входных данных.

    :param time: Строка с вводом от пользователя.
    :return: Число типа флоат.
    """
    if float(time) > 24 or float(time) < 1:
        raise ValueError
    return float(time)
