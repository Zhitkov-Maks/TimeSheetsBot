from datetime import datetime as dt, timedelta, date

from crud.statistics import aggregate_data, aggregate_data_worked_hours
from .month import get_settings
from loader import money, MONTH_DATA


async def get_salary_for_prev_month(year: int, month: int, user_id: int) -> str:
    """
    Получение первой зарплаты, которая оплачивается как количество часов
    за второй период предыдущего месяца.

    :param year: Год для агрегации.
    :param month: Месяц для агрегации.
    :param user_id: Идентификатор пользователя.
    :param currency: Валюта для отображения (по умолчанию "руб.").
    :return: Строка с информацией о зарплате.
    """
    salary: dict[str, float] = await aggregate_data(
        year, month, user_id, period=2
    )
    earned: float = salary.get("total_earned", 0)
    hours: float = salary.get("total_base_hours", 0)
    earned_hours: float = salary.get("total_earned_hours", 0)
    earned_cold: float = salary.get("total_earned_cold", 0)

    # Форматирование строки с доплатой за холод
    cold_payment = ""
    if earned_cold:
        cold_payment = (
            f"\nИз них оплата часов: {earned_hours:,.2f}{money}"
            f"\nДоплата за холод: {earned_cold:,.2f}{money}"
        )

    # Основной текст с зарплатой
    salary_info: str = (
        f"\n\nВаша 1-я ЗП:\n"
        f"-----------------------------\n"
        f"Заработано: {earned:,.2f} {money}.\n"
        f"Отработано часов: {hours:.1f}ч."
        f"{cold_payment}\n"
    )

    return salary_info


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

    cold_payment = ""
    if earned_cold:
        cold_payment = (
            f"\nИз них оплата часов: {earned_hours:,.2f}{money}."
            f"\nДоплата за холод: {earned_cold:,.2f}{money}."
        )

    message: str = (
        f"\nВаша 2-я ЗП:\n"
        f"------------------------------\n"
        f"Заработано {earned:,}{money}.\n"
        f"Отработано часов: {hours}ч."
        f"{cold_payment}\n"
    )
    
    if overtime > 0:
        message += f"Доплата за переработку: {overtime:,}{money}\n\n"

    return message


async def get_message_by_expected_salary(user_id: int) -> str:
    """
    Функция для подсчета ожидаемых ЗП в текущем месяце.

    :param user_id: Идентификатор пользователя.
    """
    # Получаем текущие год и месяц, для подсчета оплаты часов за 1 период.
    c_year, c_month = dt.now().year, dt.now().month

    # Получаем предидущий месяц, для подсчета часов за 2-й период прошлого
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
    return (f"Ожидаемые ЗП {MONTH_DATA[c_month]}/{c_year}"
            f"{message_first_pay} {message_second_pay}"
    )
