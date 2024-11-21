from datetime import datetime

from aiogram.utils.markdown import hbold
from sqlalchemy import Row


async def gen_message_statistic(data: Row[tuple], year: int) -> str:
    """
    Функция для генерации сообщения для показа статистики.
    :param year: Год для статистики.
    :param data: Общие данные за год.
    :return: Сообщение для пользователя.
    """
    total_hours: int = data[1] + data[2]
    days_in_year: int = 365
    date_now: datetime = datetime.now()

    if year == date_now.year:
        days_in_year = date_now.timetuple().tm_year

    message: str = (
        f"Ваша статистика за {hbold(year)} год.\n"
        f"{60 * "-"}\n"
        f"Заработано: {data[0]:,.2f}₽\n"
        f"Отработано часов: {hbold(total_hours)}ч\n"
        f"Из них переработки: {hbold(data[2])}ч.\n"
        f"{60 * "-"}\n"
        f"За год вы потратили на работу {int(total_hours // 24)} дней,\n"
        f"Что составляет {hbold(round(total_hours / (days_in_year * 24) * 100, 2))}% "
        f"времени в году."
    )
    return message
