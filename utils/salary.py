from datetime import datetime as dt, timedelta, date

from crud.statistics import aggregate_data, aggregate_data_worked_hours
from crud.settings import get_settings_user_by_id
from .month import get_settings
from loader import money


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
    return (f"Ваша 1 ЗП составит: "
            f"{salary.get("total_earned", 0):,}{money}.\n"
            f"За: {salary.get("total_base_hours", 0)} отработанных часов.\n\n")


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
    number_hours, overtime, cold = await get_settings(user_id)
    aggregate_hours = await aggregate_data_worked_hours(year, month, user_id)
    worked_hours = aggregate_hours.get("total_base_hours", 0)

    money_overtime: int = 0
    money_cold: int = 0

    if number_hours and overtime and worked_hours > number_hours:
        money_overtime = (worked_hours - number_hours) * overtime

    if cold:
        money_cold = worked_hours * cold

    return money_overtime, money_cold


async def generate_message_two(
        aggregate_data: dict, overtime: float, cold: float
) -> str:
    """
    Функция для формирования сообщения для пользователя.

    :param aggreagate_data: Словарь с данными за первый период текущего месяца.
    :param overtime: Сумма доплаты за переработку.
    :param cold: Сумма доплаты за холод.
    """
    earned: float = aggregate_data.get("total_earned", 0)
    hours: float = aggregate_data.get("total_base_hours", 0)
    earned += (overtime + cold)

    message: str = (f"Ваша 2 ЗП составит: {earned:,}{money}.\n"
                    f"За: {hours} отработанных часов.\n")
    
    if overtime > 0:
        message += f"Доплата за переработку: {overtime:,}{money}\n"

    if cold > 0:
        message += f"Доплата за холод: {cold:,}{money}\n"

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
    money_overtime, money_cold = await calculation_of_surcharges(
        p_year, p_month, user_id
    )

    message_second_pay = await generate_message_two(
        current_month_one_period, money_overtime, money_cold
    )
    return message_first_pay + message_second_pay
