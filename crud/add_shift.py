from typing import List

from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_conf import get_async_session
from database.models import Salary


async def write_salary_shift(salary_list: List[Salary]) -> None:
    """
    Функция для сохранения записи о смене.
    :param salary_list: Список для записи в базу данных.
    """
    session: AsyncSession = await get_async_session()
    new_salaries: List[Salary] = []

    for salary in salary_list:
        # Проверка на существование записи с тем же user_chat_id и date
        existing_record: Result[tuple[Salary]] = await session.execute(
            select(Salary).where(
                Salary.user_chat_id == salary.user_chat_id,
                Salary.date == salary.date
            )
        )
        if not existing_record.scalars().first():  # Если запись не найдена
            new_salaries.append(salary)  # Добавляем в список новых записей

    # Добавляем только новые записи
    session.add_all(new_salaries)

    try:
        await session.commit()  # Пытаемся сохранить все новые записи
    except IntegrityError:
        await session.rollback()  # Откат транзакции в случае ошибки
