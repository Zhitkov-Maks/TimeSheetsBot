from datetime import datetime as dt

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, asc, Sequence
from database.db_conf import get_async_session
from database.models import Salary


async def get_information_for_month(user_id: int, diff=0) -> Sequence:
    """Получение данных за выбранный месяц."""
    session: AsyncSession = await get_async_session()
    month: int = dt.now().month - diff
    month: str = str(month) if month > 9 else f"0{month}"
    year: int = dt.now().year

    stmt = (select(Salary)
            .where(Salary.user_chat_id == user_id)
            .where(Salary.date.ilike(f"%/{month}/{year}%"))
            .order_by(asc(Salary.date))
            )

    data = await session.execute(stmt)
    await session.close()
    return data.all()
