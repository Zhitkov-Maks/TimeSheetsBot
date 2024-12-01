from datetime import datetime as dt, timedelta, datetime, date
from typing import Tuple, List

from crud.add_shift import write_salary_shift
from database.models import Salary
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
        overtime: float,
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
    base, overtime, earned = await earned_salary(
        time=time, overtime=overtime, user_id=user_id
    )

    # Создание списка объектов Salary на основе вычисленных данных и дат
    salary_lis: List[Salary] = await create_list_salary(
        user_id, base, overtime, earned, list_dates
    )

    # Запись созданных объектов Salary в базу данных
    await write_salary_shift(salary_lis)


async def create_list_salary(
        user_id: int,
        base: float,
        overtime: float,
        earned: float,
        list_dates: List[str]
) -> List[Salary]:
    """
    Создает список объектов Salary на основе предоставленных данных. Нужна для
    добавления в бд зразу списка смен.

    :param user_id: Идентификатор пользователя (чата), для которого создаются
        записи о зарплате.
    :param base: Основное количество часов, отработанных пользователем.
    :param overtime: Количество сверхурочных часов, отработанных пользователем.
    :param earned: Общая сумма, заработанная пользователем за указанный период.
    :param list_dates: Список строковых дат в формате "YYYY-MM-DD", для которых
        необходимо создать записи о зарплате.

    :return: Список объектов Salary, созданных на основе предоставленных данных.
    """
    salary_list: List[Salary] = []

    for d in list_dates:
        # Определение периода (1 - первая половина месяца, 2 - вторая половина)
        period: int = 1 if int(date[-2:]) <= 15 else 2

        # Преобразование строки даты в объект datetime
        parse_date: date = datetime.strptime(d, "%Y-%m-%d")

        data: dict = {
            "user_chat_id": user_id,
            "base_hours": float(base),
            "overtime": float(overtime),
            "earned": float(earned),
            "date": parse_date,
            "period": period,
        }
        salary: Salary = Salary(**data)
        salary_list.append(salary)

    return salary_list
