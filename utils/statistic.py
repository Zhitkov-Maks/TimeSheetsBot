import asyncio
import calendar

from crud.statistics import aggregate_data, get_other_sum


async def get_data_from_db(year: int, month: int, user_id: int) -> tuple:
    """
    Get the calculation data from the database.
    
    :param year: The year for the request.
    :param month: The month for the request.
    :param user_id: The user's ID.
    :return tuple: A tuple with data.
    """
    return (
        await asyncio.gather(
            aggregate_data(year, month, user_id, period=1),
            aggregate_data(year, month, user_id, period=2),
            get_other_sum(year, month, user_id, "income"),
            get_other_sum(year, month, user_id, "expence"),
            return_exceptions=False
        )
    )


async def return_data(data: dict) -> tuple:
    """
    Return the data from the dictionary.
    
    :param data: The data for the year is by hours and primaries.
    """
    earned = data.get("total_earned", 0)
    award = data.get("total_award", 0)
    hours = data.get("total_hours", 0)
    sum_earned = float(earned) + float(award)
    return sum_earned, hours


async def generate_message_statistic(
    data: dict, for_other: dict, year: int
) -> str:
    """
    Generate a message for the user.
    
    :param data: Earnings for hours and bonuses.
    :param for_other: Other income.
    :param year: A year for statistics.
    """
    if len(data) == 0:
        return "Информации за выбранный год нет!"

    earned, hours = await return_data(data)
    other_earned = for_other.get("total_other_amount", 0)
    days = 366 if calendar.isleap(year) else 365

    message = "*" * 40 + "\n\n"
    message += f"Основная статистика за {year} год.\n\n"
    message += f"Всего отработано часов: {hours}ч.\n"
    message += f"Вы провели на работе {round(hours / 24, 1)} дней.\n"
    
    message += f"Что составляет {
        round((hours) / (days * 24) * 100, 1)
    }% времени в году.\n"
    
    message += f"Вы заработали: {(earned + other_earned):,}₽.\n\n"
    message += "*" * 40 + "\n\n"

    return message
