from sqlalchemy import (
    delete,
    Select,
    select,
    Sequence,
    Delete,
    ScalarResult,
)
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_conf import get_async_session
from database.models import Remind


async def add_user_time(time: int, user: int) -> None:
    """
    Добавляет настройки для уведомлений.
    :param time: Новое время уведомлений.
    :param user: ID пользователя телеграм у которого нужно обновить время.
    :return None:
    """
    session: AsyncSession = await get_async_session()
    remind: Remind = Remind(
        user_chat_id=user,
        time=time,
    )
    session.add(remind)
    await session.commit()


async def upgrade_time(time: int, user: int) -> None:
    """
    Обновляет время уведомлений.
    :param time: Новое время уведомлений
    :param user: Пользователь у которого нужно обновить время.
    :return None:
    """
    session: AsyncSession = await get_async_session()
    stmt: Select = select(Remind).filter(Remind.user_chat_id == user)
    remind: Remind = await session.scalar(stmt)

    if remind is not None:
        remind.time = time
        await session.commit()
    else:
        pass


async def remove_time(user: int) -> None:
    """
    Удаляет настройки уведомлений.
    :param user: Пользователь которому нужно удалить настройки.
    :return None:
    """
    session: AsyncSession = await get_async_session()
    stmt: Delete = delete(Remind).where(Remind.user_chat_id == user)
    await session.execute(stmt)
    await session.commit()


async def get_all_users() -> Sequence:
    """
    Функция для получения списка пользователей у которых есть настройка
    уведомлений.
    :return: Список напоминаний, в которых есть user_chat_id.
    """
    session: AsyncSession = await get_async_session()
    stmt: Select = select(Remind)
    data: ScalarResult[Remind] = await session.scalars(stmt)

    await session.close()
    return data.all()
