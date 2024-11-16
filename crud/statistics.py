from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, asc, Sequence
from database.db_conf import get_async_session
from database.models import Salary


async def get_information_for_month(user_id: int, year, month) -> Sequence:
    """Получение данных за выбранный месяц."""
    session: AsyncSession = await get_async_session()
    month: str = str(month) if month > 9 else f"0{month}"

    stmt = (select(Salary)
            .where(Salary.user_chat_id == user_id)
            .where(Salary.date.ilike(f"%/{month}/{year}%"))
            .order_by(asc(Salary.date))
            )

    data = await session.execute(stmt)
    await session.close()
    return data.all()


async def get_info_by_date(user_id: int, date: str) -> Salary:
    session: AsyncSession = await get_async_session()
    stmt = (select(Salary)
            .where(Salary.user_chat_id == user_id)
            .where(Salary.date.ilike(date))
            )
    data = await session.scalar(stmt)
    await session.close()
    return data
