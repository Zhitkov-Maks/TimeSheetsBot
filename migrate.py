from alembic.config import Config
from alembic import command
from sqlalchemy.ext.asyncio import create_async_engine

from config import DB_USER, DB_PASS, DB_NAME

# Настройка подключения к базе данных
DATABASE_URL: str = "postgresql+asyncpg://{0}:{1}@db_bot/{2}".format(
    DB_USER,
    DB_PASS,
    DB_NAME,
)


def run_migrations():
    # Создаем подключение к базе данных
    engine = create_async_engine(DATABASE_URL, echo=False)

    # Настройка Alembic
    alembic_cfg = Config(
        "alembic.ini"
    )  # Убедитесь, что файл alembic.ini находится в корне проекта
    alembic_cfg.attributes["connection"] = engine

    # Выполняем миграции
    command.upgrade(alembic_cfg, "head")


if __name__ == "__main__":
    run_migrations()
