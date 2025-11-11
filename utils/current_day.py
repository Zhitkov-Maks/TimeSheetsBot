"""Auxiliary module for calculating salaries for a selected day."""
from datetime import datetime, UTC
from crud.create import delete_record, write_salary
from loader import MONTH_DATA, money
from crud.settings import get_settings_user_by_id
from crud.get_data import get_hours_for_month, get_salary_for_day, update_salary
from utils.valute import get_valute_info
from utils.calculate import calc_valute


async def get_settings(user_id: int) -> tuple[float]:
    """
    Return the basic user settings.
    
    :param user_id: The user's ID.
    """
    settings: dict = await get_settings_user_by_id(user_id)
    if not settings:
        raise KeyError("Нет настроек для рассчета.")

    price: float = float(settings.get("price_time", 0))
    cold: float = float(settings.get("price_cold", 0))
    overtime: float = float(settings.get("price_overtime", 0))
    award: float = float(settings.get("price_award", 0))
    return price, cold, overtime, award


async def calculation_overtime(
    settings: tuple[float],
    time: float,
    norm: int,
    total_hours: float
) -> tuple:
    """
    Calculate how much the user earned per shift 
    if he has already overworked by the hour.
    
    :param settings: User settings.
    :param time: Time worked.
    :param norm: The standard of hours per month.
    :param total_hours: How many hours have been worked already this month.
    :return dict: A tuple with data to save.
    """
    price, cold, overtime, _ = settings
    time_over = (time + total_hours) - norm
    earned = round(
        min(time_over, time) * (price + overtime) + \
        max((time - time_over), 0) * price, 2
    )
    return earned, min(time_over, time), overtime * min(time_over, time)


async def earned_calculation(
    settings: tuple[float],
    time: float,
    user_id: int,
    date,
) -> dict[str, float]:
    """
    Create a dictionary for future storage in the database.
    
    :param settings: User settings.
    :param time: Time worked.
    :param user_id: User's ID.
    :param date: The date for adding the shift.
    :return dict: Dictionary with the configuration for writing.
    """
    configuration: dict[str, float] = dict()
    year, month = date.year, date.month
    total_hours: tuple[float] = await get_hours_for_month(user_id, year, month)
    norm_hours = 180 if month == 2 else 190
    
    earned_time = time * settings[0]
    earned_cold = time * settings[1]

    if settings[2] > 0 and (time + total_hours) > norm_hours:
        (
            earned_time,
            hours_overtime,
            earned_overtime
        ) = await calculation_overtime(settings, time, norm_hours, total_hours)

        configuration.update(
            hours_overtime=hours_overtime,
            earned_overtime=earned_overtime
        )

    configuration.update(
        base_hours=time,
        earned=(earned_time + earned_cold),
        earned_hours=earned_time - earned_overtime,
        earned_cold=earned_cold
    )
    return configuration


async def earned_per_shift(
    time: float,
    user_id: int,
    date: str,
    data: dict
) -> tuple[float, float]:
    """
    Generate the amount earned per shift..

    :param time: Hours worked.
    :param user_id: The user's ID.
    :return: The earned amount for the month.
    :param date: The date for recording.
    """
    action = data.get("action")
    settings: tuple[float] = await get_settings(user_id)
    parse_date = datetime.strptime(date, "%Y-%m-%d")

    notes: str = ""
    if action == "change":
        notes = data.get("current_day").get("notes", {})
        await delete_record(date, user_id)

    salary = await earned_calculation(settings, time, user_id, parse_date)

    if action == "change" and notes:
        salary.update(notes=notes)

    valute_data: dict[str, tuple[int, float]] = await get_valute_info()
    await write_salary(salary, user_id, parse_date, valute_data)
    return salary.get("earned")


async def gen_message_for_choice_day(salary: dict, choice_date: str) -> str:
    """
    Generate salary messages for the selected shift for the user.

    :param choice_date: The transmitted date from the calendar.
    :param salary: Earnings for a certain day.
    :return: A message for the user.
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
    if salary.get("award_amount") is not None:
        count: int = int(salary.get("count_operations", 0))
        detail_message += (
            f"Премия: {salary.get("award_amount")}{money}({count})\n"
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
    Check the input data.

    :param time: A string with user input.
    :return: A float type number.
    """
    if float(time) > 24 or float(time) < 1:
        raise ValueError
    return float(time)


async def calc_in_currency(earned: float) -> float:
    current_valute: dict[str, float] = await get_valute_info()
    return await calc_valute(earned, current_valute)


async def earned_for_award(
    count_operations: int,
    user_id: int,
    day_id: str,
) -> dict:
    """
    Calculate the bonus and update the salary record.
    
    :param count_operations: The number of operations performed by the user.
    :param user_id: The user's ID.
    :param day_id: ID of the day.
    :return dict: Dictionary with shift data.
    """
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
        
    currency: float = await calc_in_currency(earned)
    current_day.update(
        award_amount=earned_award,
        count_operations=count_operations,
        earned=earned,
        valute=currency
    )
    await update_salary(day_id, current_day)
    return current_day
