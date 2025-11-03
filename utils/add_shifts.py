from datetime import datetime as dt, timedelta, datetime, date, UTC
from typing import Tuple, List

from crud.add_shift import add_many_shifts
from utils.current_day import earned_salary
from utils.valute import get_valute_info
from utils.calculate import calc_valute


async def get_date(action: str) -> Tuple[int, int]:
    """
    Функция для получения месяца и года для дальнейшей работы с ними.

    :param action: Строка, определяющая действие.
    :return: Кортеж из двух целых чисел: (год, месяц).
    """
    year, month = int(action.split("-")[0]), int(action.split("-")[1])
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
    :param list_dates: Список строковых дат в формате "YYYY-MM-DD", для которых
        необходимо создать записи о сменах.
    :return: None.
    """
    # Вычисление базовой зарплаты и общей заработанной суммы.
    base, earned_hours, earned_cold = await earned_salary(time, user_id)

    # Создание списка объектов Salary на основе вычисленных данных и дат
    salary_lis = await create_list_salary(
        user_id, base, earned_hours, earned_cold, list_dates
    )

    # Запись созданных объектов Salary в базу данных
    await add_many_shifts(salary_lis)


async def create_list_salary(
        user_id: int,
        base: float,
        earned_hours: float,
        earned_cold: float,
        list_dates: List[str]
) -> list[dict]:
    """
    Создает список объектов Salary на основе предоставленных данных.
    Нужна для добавления в бд зразу списка смен.
    """
    salary_list = []
    valute_data: dict[str, tuple[int, float]] = await get_valute_info()

    for d in list_dates:
        # Определение периода (1 - первая половина месяца, 2 - вторая половина)
        period: int = 1 if int(str(d)[-2:]) <= 15 else 2

        # Преобразование строки даты в объект datetime
        parse_date: date = datetime.strptime(d, "%Y-%m-%d")
        earned: float = earned_hours + earned_cold
        earned_in_valute = await calc_valute(earned, valute_data)

        data: dict = {
            "user_id": user_id,
            "date": parse_date,
            "base_hours": float(base),
            "earned": float(earned),
            "earned_hours": earned_hours,
            "earned_cold": earned_cold,
            "period": period,
            "valute": earned_in_valute,
            "date_write": dt.now(UTC)
        }
        salary_list.append(data)

    return salary_list
