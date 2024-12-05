from aiogram.utils.markdown import hbold
from sqlalchemy import Row
from typing import Tuple, List


async def gen_message_statistic(
        data: Row[List[Tuple[int]]],
        year: int
) -> str:
    """
    Функция для генерации сообщения для показа статистики.
    :param year: Год для статистики.
    :param data: Общие данные за год.
    :return: Сообщение для пользователя.
    """
    total_hours: int = data[1] + data[2]
    total_earned: int = data[0] + data[3]
    days_in_year: int = 365

    message: str = (
        f"Ваша статистика за {hbold(year)} год.\n\n"
        f"Заработано: {total_earned:,.2f}₽\n"
        f"Отработано часов: {hbold(total_hours)}ч\n"
        f"Из них переработки: {hbold(data[2])}ч.\n"
        f"Что составляет {hbold(round((data[2] / (data[1] + data[2])) * 100, 2))}%\n\n"
        f"За год вы потратили на работу {int(total_hours // 24)} дней,\n"
        f"Что составляет {hbold(round((total_hours / (days_in_year * 24)) * 100, 2))}% "
        f"времени в году."
    )
    return message
