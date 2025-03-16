from datetime import datetime as dt, timedelta, datetime, date
from typing import Tuple, List

from crud.add_shift import write_salary_shift
from utils.current_day import earned_salary


async def get_date(action: str) -> Tuple[int, int]:
    """
    Функция для получения месяца и года для дальнейшей работы с ними.

    :param action: Строка, определяющая действие.
                   Если 'current', возвращает текущий месяц и год.
                   Иначе возвращает следующий месяц.

    :return: Кортеж из двух целых чисел: (год, месяц).
    """
    date_current: dt = dt.now()
    year, month = date_current.year, date_current.month
    if action == "next_month":
        next_date: date = date(year, month, 1) + timedelta(days=35)
        year, month = next_date.year, next_date.month

    return year, month


async def create_data_by_add_shifts(
        user_id: int,
        time: float,
        list_dates: List[str]
) -> None:
    """
    Создает записи о сменах для пользователя на основе предоставленных данных.

    :param user_id: Идентификатор пользователя (чата), для которого создаются
        записи о сменах.
    :param time: Общее количество отработанных часов.
    :param overtime: Количество сверхурочных часов.
    :param list_dates: Список строковых дат в формате "YYYY-MM-DD", для которых
        необходимо создать записи о сменах.

    :return: None
    """
    # Вычисление базовой зарплаты, сверхурочных и общей заработанной суммы
    base, earned, earned_cold = await earned_salary(time, user_id)

    # Создание списка объектов Salary на основе вычисленных данных и дат
    salary_lis = await create_list_salary(
        user_id, base, earned, earned_cold, list_dates
    )

    # Запись созданных объектов Salary в базу данных
    await write_salary_shift(salary_lis)


async def create_list_salary(
        user_id: int,
        base: float,
        earned: float,
        earned_cold: float,
        list_dates: List[str]
):
    """
    Создает список объектов Salary на основе предоставленных данных.
    Нужна для добавления в бд зразу списка смен.
    """
    salary_list = []

    for d in list_dates:
        # Определение периода (1 - первая половина месяца, 2 - вторая половина)
        period: int = 1 if int(str(d)[-2:]) <= 15 else 2

        # Преобразование строки даты в объект datetime
        parse_date: date = datetime.strptime(d, "%Y-%m-%d")

        data: dict = {
            "user_id": user_id,
            "date": parse_date,
            "data": {
                "base_hours": float(base),
                "earned": float(earned),
                "period": period,
                "earned_cold": earned_cold
            }
        }
        salary_list.append(data)

    return salary_list
