"""Вспомогательный модуль для подсчета зарплаты за выбранный день."""

from loader import MONTH_DATA
from crud.settings import get_settings_user_by_id


async def earned_per_shift(base: float, user_id: int) -> float:
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

    price: float = settings.get("price_time")
    earned: float = float(price) * base
    return earned


async def earned_salary(time: float, user_id: int) -> tuple:
    """
    Промежуточная функция, для получения нужных нам данных
    для вывода сообщения.
    :param time: Отработанное время.
    :param overtime: Переработано.
    :param user_id: Id пользователя.
    :return: Кортеж с временем, переработкой, заработком.
    """
    earned = await earned_per_shift(time, user_id)
    return time, earned


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
        f"{salary.get("base_hours")} часов.\n"
        f"Заработали: {salary.get("earned")}₽.\n"
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
