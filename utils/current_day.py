"""Вспомогательный модуль для подсчета зарплаты за выбранный день."""

from loader import MONTH_DATA, money
from crud.settings import get_settings_user_by_id
from crud.get_data import get_salary_for_day, update_salary


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
        detail_message += (
            f"Доплата за холод: {salary.get("earned_cold")}{money}.\n"
        )
    if salary.get("award_amount"):
        detail_message += (
            f"Примия: {salary.get("award_amount")}{money}.\n"
        )

    return (
        f"Информация за {MONTH_DATA[month]} {day}.\n"
        f"--------------------------------------------\n"
        f"Отработано часов: {salary.get("base_hours")}ч.\n"
        f"Заработано: {salary.get("earned")}{money}.\n"
        f"Оплата часов: {salary.get('earned_hours')}{money}.\n"
        f"{detail_message}"
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


async def earned_for_award(
    count_operations: int,
    user_id: int,
    day_id: str,
) -> str:
    """Посчитай премию и обнови запись о зп."""
    settings: dict = await get_settings_user_by_id(user_id)
    cost_award = settings.get("price_award")
    if cost_award is None:
        raise ValueError("Нет данных о стоимости операции!")

    earned_award: float = round(count_operations * float(cost_award), 2)
    current_day: dict = await get_salary_for_day(day_id)

    if current_day.get("award_amount"):
        earned = (
            current_day["earned"] - current_day["award_amount"] + earned_award
        )
    else:
        earned = earned_award + current_day["earned"]

    current_day.update(
        award_amount=earned_award,
        earned=earned
    )
    await update_salary(day_id, current_day)
    return current_day
