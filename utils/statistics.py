"""A module for generating a message with statistics."""
from aiogram.utils.markdown import hbold


async def generate_text(one, two, total) -> str:
    """Непосредственно формирование сообщения."""
    return f"""
Подводим итоги ✊😎💪
{70 * "-"}
За первый период заработано: {hbold(one[0])}₽ 
Отработано - {hbold(one[1])} ч 
В т.ч доп часов - {hbold(one[2])} ч
{70 * "-"}
За второй период заработано: {hbold(two[0])}₽
Отработано - {hbold(two[1])} ч
В т.ч доп часов - {hbold(two[2])} ч
{70 * "-"}
За весь месяц заработано: {hbold(total[0])}₽
Отработано - {hbold(total[1])} ч
В т.ч доп - {hbold(total[2])} ч
{70 * "-"}
"""


async def generate_statistics(info: list):
    """
    Объединяет часы в общие. И если у нас по выбранному
    месяцу ничего нет то заменяет None нулями.
    """
    if info[0] is None:
        info[0], info[1], info[2] = 0, 0, 0
    else:
        info[1] = info[1] + info[2]
    return info


async def total_info(one: tuple, two: tuple, total: tuple) -> str:
    """Запуск формирования сообщения со статистикой."""
    info_one: list = await generate_statistics(list(one))
    info_two: list = await generate_statistics(list(two))
    info_total: list = await generate_statistics(list(total))
    return await generate_text(info_one, info_two, info_total)
