from calendar import monthrange
from datetime import datetime

from crud.settings import get_settings_user_by_id
from database import Settings
from keywords.add_shifts import days_choices
from keywords.prediction import user_choices, hour_choices
from utils.current_day import Employee
from utils.prediction import parse_data


async def get_prediction_sum(user_id: int, data_: dict) -> int:
    """
    Функция для вычисления ожидаемой зп в пятидневку.
    :param user_id: Id юзера.
    :param data_: Дополнительные данные.
    :return: Прогнозируемую сумму.
    """
    month, year, weekdays, hours = await parse_data(data_)
    price: Settings | None = await get_settings_user_by_id(user_id)

    if price is None:
        price: Employee = Employee(300, 100)

    # Получаем количество дней в месяце.
    days_in_month: int = monthrange(year, int(month))[1]
    month: str = str(month) if int(month) > 9 else f"0{month}"

    total_sum: int = 0
    for i in range(1, days_in_month + 1):
        days: str = str(i) if i > 9 else f"0{i}"
        wd = datetime.strptime(
            f"{days}-{month}-{year}", "%d-%m-%Y"
        ).weekday()

        delay: str | list = data_.get("delay")
        hour: int = int(data_.get("hour"))

        if delay == "delay_no":
            if wd in (range(5)):
                total_sum += price.price * hours

        else:
            if wd in delay:
                total_sum += price.price * hours + (
                        price.price + price.overtime) * hour
            elif wd in (range(5)):
                total_sum += price.price * hours

    total_sum += ((price.price + price.overtime) * hours) * weekdays
    return total_sum


async def clear_data(user_chat_id: int) -> None:
    """
    Очищаем словари от данных.
    """
    user_choices[user_chat_id].clear()
    hour_choices[user_chat_id].clear()
    days_choices[user_chat_id].clear()
