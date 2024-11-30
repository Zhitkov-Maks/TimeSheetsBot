from datetime import datetime as dt, timedelta, datetime
from typing import Tuple, List

from crud.add_shift import write_salary_shift
from database.models import Salary
from utils.count import earned_salary


async def get_date(action: str) -> Tuple[int, int]:
    """
    Функция для получения месяца и года для дальнейшей работы с ними.

    :param action: Строка, определяющая действие.
                   Если 'current', возвращает текущий месяц и год.
                   Если любое другое значение, возвращает месяц и год через
                   30 дней.

    :return: Кортеж из двух целых чисел: (год, месяц).
    """
    if action == "current":
        # Получение текущей даты и времени
        date_current: dt = dt.now()

        # Возврат текущего года и месяца
        return date_current.year, date_current.month

    else:
        # Получение даты через 30 дней от текущей
        next_date: dt = dt.now() + timedelta(days=30)

        # Возврат года и месяца через 30 дней
        return next_date.year, next_date.month


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
        time=time,
        overtime=overtime,
        user_id=user_id
    )

    # Создание списка объектов Salary на основе вычисленных данных и дат
    salary_lis: List[Salary] = await create_list_salary(
        user_id,
        base,
        overtime,
        earned,
        list_dates
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
    salary_list: List[
        Salary] = []  # Инициализация списка для хранения объектов Salary

    for date in list_dates:
        # Определение периода (1 - первая половина месяца, 2 - вторая половина)
        period: int = 1 if int(date[-2:]) <= 15 else 2

        # Преобразование строки даты в объект datetime
        parse_date: date = datetime.strptime(date, "%Y-%m-%d")

        # Создание словаря с данными для объекта Salary
        data: dict = {
            "user_chat_id": user_id,
            "base_hours": float(base),
            "overtime": float(overtime),
            "earned": float(earned),
            "date": parse_date,
            "period": period,
        }

        # Создание объекта Salary с использованием распаковки словаря
        salary: Salary = Salary(**data)

        # Добавление созданного объекта Salary в список
        salary_list.append(salary)

    return salary_list  # Возврат списка объектов Salary
