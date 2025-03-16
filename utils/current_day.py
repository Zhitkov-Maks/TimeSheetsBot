"""Вспомогательный модуль для подсчета зарплаты за выбранный день."""

from loader import MONTH_DATA
from crud.settings import get_settings_user_by_id


async def earned_per_shift(base: float, user_id: int) -> tuple:
    """
    Формируем сумму, заработанную за смену.

    :param base: Базовая ставка.
    :param overtime: Доплата за переработку.
    :param user_id: Id юзера.
    :return: Заработанную сумму за месяц.
    """
    settings: dict = await get_settings_user_by_id(user_id)
    if not settings:
        return KeyError("Я не нашел ваших настроек по оплате труда.")

    price: float = settings.get("data").get("price_time")
    price_cold: int = settings.get("data").get("price_cold")

    earned: float = float(price) * base
    earned_cold: float = base * float(price_cold)
    return earned, earned_cold


async def earned_salary(time: float, user_id: int) -> tuple:
    """
    Промежуточная функция, для получения нужных нам данных
    для вывода сообщения.
    :param time: Отработанное время.
    :param overtime: Переработано.
    :param user_id: Id пользователя.
    :return: Кортеж с временем, переработкой, заработком.
    """
    earned, earned_cold = await earned_per_shift(time, user_id)
    return time, earned, earned_cold


async def gen_message_for_choice_day(salary, choice_date: str) -> str:
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

    return (
        f"{day_month}. \nВы отработали: "
        f"{salary.get("data").get("base_hours")} часов.\n"
        f"Заработали: {salary.get("data").get("earned")}₽.\n"
        f"Доплата за холод составит: {salary.get("data").get("earned_cold")}₽\n"
    )


async def valid_time(time: str) -> float:
    """
    Небольшая проверка входных данных.

    :param time: Строка с вводом от пользователя.
    :return: Число типа флоат.
    """
    if float(time) > 24 or float(time) < 1:
        raise ValueError
    return float(time)
