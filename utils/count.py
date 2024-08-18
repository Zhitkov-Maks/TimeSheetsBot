from typing import List
from crud.settings import get_settings_user_by_id
from database import Settings


class Employee:
    """
    Класс нужен если пользователь, не сделал настройки под себя,
    тогда делаем значение по умолчанию.
    """
    def __init__(self, price, overtime):
        self.price = price
        self.overtime = overtime


async def earned_per_shift(base: int, overtime: int, user_id: int) -> int:
    """Формируем сумму, заработанную за смену."""
    settings: Settings | Employee = await get_settings_user_by_id(user_id)
    if settings is None:
        settings = Employee(300, 100)
    return (
            int(base) * settings.price +
            int(overtime) * (settings.price + settings.overtime)
    )


async def earned_salary(
        num_list: List[str],
        user_id: int
) -> tuple:
    """
    Промежуточная функция, для получения нужных нам данных
    для вывода сообщения.
    """
    base = int(num_list[0])
    overtime = int(num_list[1]) if len(num_list) > 1 else 0

    earned: int = await earned_per_shift(
        base,
        overtime,
        user_id
    )
    return base, overtime, earned
