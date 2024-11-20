from typing import Dict

from sqlalchemy import select, update, Select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from database import Settings
from database.db_conf import get_async_session


async def update_data_settings(
    data_settings: Dict[str, int], session: AsyncSession
) -> None:
    """
    Функция для обновления данных в таблице с настройками,
    чтобы у одного пользователя была только одно запись.
    :param data_settings: Словарь с id user и данными о заработках.
    :param session: AsyncSession.
    :return: None.
    """
    stmt: update = (
        update(Settings)
        .where(Settings.user_chat_id == data_settings["chat_id"])
        .values(price=data_settings["price"], overtime=data_settings["overtime"])
    )
    await session.execute(stmt)
    await session.commit()


async def write_settings(data_settings: Dict[str, str | int]) -> None:
    """
    Функция для сохранения и обновления настроек пользователя.
    :param data_settings: Словарь с данными для записи.
    :return: None.
    """
    session: AsyncSession = await get_async_session()

    request_data: Dict[str, str | int] = {
        "user_chat_id": data_settings["chat_id"],
        "price": data_settings["price"],
        "overtime": data_settings["overtime"],
    }

    if not data_settings["update"]:
        settings: Settings = Settings(**request_data)
        session.add(settings)
        await session.commit()

    else:
        # Посылаем на обновления, так как запись уже существует
        await update_data_settings(data_settings, session)


async def get_settings_user_by_id(user_chat_id: int) -> Settings:
    """
    Функция для проверки существования пользовательских настроек.
    :param user_chat_id: Id пользователя.
    :return: Настройки пользователя.
    """
    session: AsyncSession = await get_async_session()
    stmt: Select = select(Settings).where(Settings.user_chat_id == user_chat_id)
    data: ScalarResult[Settings] = await session.scalars(stmt)
    await session.close()
    return data.first()
