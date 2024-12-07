from calendar import monthrange
from typing import Dict

from typing_extensions import Tuple

from crud.settings import get_settings_user_by_id
from database import Settings
from utils.current_day import Employee
from utils.prediction import get_total_price, parse_data


async def two_in_two_get_prediction_sum(
        user_id: int, data_: Dict[str, int]
) -> Tuple[int] | Tuple[int, int]:
    """
    Функция для получения итоговой зп.
    :param user_id: Id пользователя.
    :param data_: Дополнительные данные в виде словаря для вычислений.
    :return: Прогнозируемую сумму.
    """
    month, year, weekdays, hours = await parse_data(data_)

    price: Settings | None = await get_settings_user_by_id(user_id)

    if price is None:
        price: Employee = Employee(300, 100)

    # Получаем количество дней в месяце.
    days_in_month: int = monthrange(year, month)[1]

    # Первая смена в месяце.
    first_day: int = data_.get("first_day")

    # Если первая смена второго или дальше, то проблем нет и просто считаем сумму.
    if first_day > 1:
        total_sum: int = await get_total_price(
            first_day, days_in_month, price, weekdays, hours)
        return total_sum,

    else:
        # Первый вариант если смены 1 и 2 числа.
        total_sum: int = await get_total_price(
            first_day, days_in_month, price, weekdays, hours
        )

        # Второй вариант, если смена 1, а 2 выходной.
        total_sum_two: int = await get_total_price(
            first_day + 3, days_in_month, price, weekdays, hours
        )
        sum_by_day = price.price * hours
        return total_sum, int(total_sum_two + sum_by_day)
