from datetime import datetime as dt, timedelta, date

from crud.statistics import aggregate_data, aggregate_data_worked_hours
from .month import get_settings
from loader import money, MONTH_DATA


async def get_salary_for_prev_month(
        year: int, month: int, user_id: int
) -> str:
    """
    Получение первой зарплаты. Которая оплачиваеться как 
    количество часов за второй период предидущего месяца.

    :param year: Год для аггрегации.
    :param month: Месяц для аггрегации.
    :param user_id: Идентификатор пользователя.
    """
    salary: dict[str, float] = await aggregate_data(
        year, month, user_id, period=2
    )
    earned: float = salary.get("total_earned", 0)
    hours: float = salary.get("total_base_hours", 0)
    earned_hours: float = salary.get("total_earned_hours", 0)
    earned_cold: float = salary.get("total_earned_cold", 0)

    money_cold = ""
    if earned_cold:
        money_cold += f"""Из них оплата часов: {earned_hours:,}{money}.
Доплата за холод: {earned_cold:,}{money}.
"""
        
    return f"""
Ваша 1-я ЗП:
------------------------------
Заработано: {earned:,}{money}.
Отработано часов: {hours}ч.
{money_cold}"""


async def calculation_of_surcharges(
        year: int, month: int, user_id: int
) -> tuple[float, float]:
    """
    Функция для подсчета надбавок, таких как переработки и 
    доплата за холод. Доплаты начисляються за прошедший месяц.

    :param year: Год для аггрегации.
    :param month: Месяц для аггрегации.
    :param user_id: Идентификатор пользователя.
    """
    overtime, _ = await get_settings(user_id)
    aggregate_hours = await aggregate_data_worked_hours(year, month, user_id)
    worked_hours = aggregate_hours.get("total_base_hours", 0)

    hours = 190 if month != 2 else 180 # Норма часов в месяц.

    money_overtime: float = 0.0
    if overtime and worked_hours > hours:
        money_overtime = (worked_hours - hours) * overtime

    return money_overtime


async def generate_message_two(
        aggregate_data: dict, overtime: float) -> str:
    """
    Функция для формирования сообщения для пользователя.

    :param aggreagate_data: Словарь с данными за первый период текущего месяца.
    :param overtime: Сумма доплаты за переработку.
    :param cold: Сумма доплаты за холод.
    """
    earned: float = aggregate_data.get("total_earned", 0)
    hours: float = aggregate_data.get("total_base_hours", 0)
    earned_hours: float = aggregate_data.get("total_earned_hours", 0)
    earned_cold: float = aggregate_data.get("total_earned_cold", 0)
    earned += overtime

    money_cold = ""
    if earned_cold:
        money_cold += f"""Из них оплата часов: {earned_hours:,}{money}.
Доплата за холод: {earned_cold:,}{money}."""

    message: str = f"""
Ваша 2-я ЗП:
------------------------------
Заработано {earned:,}{money}."
За: {hours} отработанных часов.
{money_cold}
"""

    if overtime > 0:
        message += f"Доплата за переработку: {overtime:,}{money}\n"

    return message


async def get_message_by_expected_salary(user_id: int) -> str:
    """
    Функция для подсчета ожидаемых ЗП в текущем месяце.

    :param user_id: Идентификатор пользователя.
    """
    # Получаем текущие год и месяц, для подсчета оплаты часов за 1 период.
    c_year, c_month = dt.now().year, dt.now().month

    # Получаем придидущий месяц, для подсчета часов за 2-й период прошлого
    # месяца и суммы отработанных часов за прошлый месяц для рассчета доплат.
    prev_date = date(c_year, c_month, 1) - timedelta(days=10)
    p_year, p_month = prev_date.year, prev_date.month

    message_first_pay: str = await get_salary_for_prev_month(
        p_year, p_month, user_id
    )
    
    current_month_one_period = await aggregate_data(
        c_year, c_month, user_id, period=1
    )
    money_overtime: float = await calculation_of_surcharges(
        p_year, p_month, user_id
    )

    message_second_pay = await generate_message_two(
        current_month_one_period, money_overtime
    )
    return f"""Ожидаемые ЗП {MONTH_DATA[c_month]}/{c_year}
{message_first_pay} {message_second_pay}
"""
