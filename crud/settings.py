from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import Settings
from database.db_conf import get_async_session


async def update_data_settings(data_settings, session: AsyncSession) -> None:
    """
    Функция для обновления данных в таблице с настройками,
    чтобы у одного пользователя была только одно запись.
    """
    stmt = (update(Settings)
            .where(Settings.user_chat_id == data_settings["chat_id"])
            .values(
        price=data_settings["price"], overtime=data_settings["overtime"])
    )
    await session.execute(stmt)
    await session.commit()


async def write_settings(data_settings: dict) -> None:
    """Функция для сохранения настроек пользователя."""
    session: AsyncSession = await get_async_session()

    request_data: dict = {
        "user_chat_id": data_settings["chat_id"],
        "price": data_settings["price"],
        "overtime": data_settings["overtime"]
    }

    if not data_settings["update"]:
        settings: Settings = Settings(**request_data)
        session.add(settings)
        await session.commit()

    else:
        # Посылаем на обновления, так как запись уже существует
        await update_data_settings(data_settings, session)


async def get_settings_user_by_id(user_chat_id: int) -> Settings:
    """Функция для проверки существования пользовательских настроек."""
    session: AsyncSession = await get_async_session()
    stmt = (
        select(Settings)
        .where(Settings.user_chat_id == user_chat_id)
    )
    data = await session.scalars(stmt)
    await session.close()
    return data.first()
