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


async def earned_per_shift(base: float, overtime: float, user_id: int) -> int:
    """Формируем сумму, заработанную за смену."""
    settings: Settings | Employee = await get_settings_user_by_id(user_id)
    if settings is None:
        settings = Employee(300, 100)
    return round(
            base * settings.price +
            overtime * (settings.price + settings.overtime), 2
    )


async def earned_salary(
        time: float,
        overtime: float,
        user_id: int
) -> tuple:
    """
    Промежуточная функция, для получения нужных нам данных
    для вывода сообщения.
    """
    earned: int = await earned_per_shift(
        time,
        overtime,
        user_id
    )
    return time, overtime, earned
