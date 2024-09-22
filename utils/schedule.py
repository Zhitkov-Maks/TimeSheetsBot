from sqlalchemy.ext.asyncio import AsyncSession

from database import Settings
from database.db_conf import get_async_session
from sqlalchemy import select, Sequence, Select


async def get_all_users() -> Sequence:
    session: AsyncSession = await get_async_session()
    stmt: Select = select(Settings)
    data = await session.execute(stmt)
    await session.close()
    return data.all()
