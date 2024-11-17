from sqlalchemy import (
    delete,
    Select,
    select,
    Sequence,
    Delete,
    ScalarResult,
)
from sqlalchemy.exc import IntegrityError, ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_conf import get_async_session
from database.models import Remind


async def add_user_time(time: int, user: int) -> None:
    """
    Добавляет настройки для уведомлений.
    :param time: Новое время уведомлений.
    :param user: Пользователь у которого нужно обновить время.
    :return None:
    """
    session = await get_async_session()
    remind: Remind = Remind(
        user_chat_id=user,
        time=time,
    )
    try:
        session.add(remind)
        await session.commit()
    except IntegrityError:
        pass


async def upgrade_time(time: int, user: int) -> None:
    """
    Обновляет время уведомлений.
    :param time: Новое время уведомлений
    :param user: Пользователь у которого нужно обновить время.
    :return None:
    """
    session = await get_async_session()
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
    session = await get_async_session()
    stmt: Delete = delete(Remind).where(Remind.user_chat_id == user)
    await session.execute(stmt)
    await session.commit()


async def get_settings_all() -> Sequence:
    """
    Функция возвращает список пользователей у которых имеются настройки
    для уведомлений. Код обернут в try except по причине того что при первом
    запуске проекта база еще не создана, а у нас сразу выполняется запрос
    на получение пользователей у которых настроено уведомление и приложение
    падает с ошибкой.
    :return Sequence: Список пользователей и время для показа уведомлений.
    """
    session = await get_async_session()
    try:
        stmt = select(Remind)
        results: ScalarResult = await session.scalars(stmt)
        return results.all()
    except ProgrammingError:
        pass


async def get_all_users() -> Sequence:
    session: AsyncSession = await get_async_session()
    stmt: Select = select(Remind)
    data = await session.scalars(stmt)
    await session.close()
    return data.all()
