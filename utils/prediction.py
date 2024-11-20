from calendar import monthrange
from datetime import datetime

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import Settings
from database.db_conf import get_async_session
from utils.count import Employee


async def get_prediction_sum(month: int, year: int, user_id: int) -> int:
    """
    Функция для вычисления ожидаемой зп. Подсчет основан на том основании,
    что у меня один доп и 2 раза в неделю остаюсь до семи.
    :param month: Месяц выбранный.
    :param year: Выбранный год.
    :param user_id: Id юзера.
    :return: Прогнозируемую сумму.
    """
    # Получим настройки стоимости для конкретного пользователя
    session: AsyncSession = await get_async_session()
    stmt: Select = select(Settings).where(Settings.user_chat_id == user_id)
    price: Settings | None = await session.scalar(stmt)
    if price is None:
        price: Employee = Employee(300, 100)

    # Получаем количество дней в месяце.
    days_in_month: int = monthrange(year, month)[1]
    month: str = str(month) if month > 9 else f"0{month}"

    total_sum: int = 0
    for i in range(1, days_in_month + 1):
        days: str = str(i) if i > 9 else f"0{i}"
        wd = datetime.strptime(f"{days}-{month}-{year}", "%d-%m-%Y").weekday()
        if wd in (1, 3):
            total_sum += price.price * 9 + (price.price + price.overtime) * 2
        elif wd in (0, 2, 4):
            total_sum += price.price * 9

    total_sum += (price.price + price.overtime) * 9
    await session.close()
    return total_sum
