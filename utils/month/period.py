from aiogram.fsm.context import FSMContext

from .month import get_settings, data_calculation, get_data_from_db

from loader import money


async def get_message_for_period(data: tuple, name: str) -> str:
    """
    Create a message to send to the user.
    
    :param data: A tuple with the necessary data.
    :param name: The name of the command.
    """
    number = f"{name[-1]} период" if name[-1].isdigit() else "месяц!"
    message = f"Информация за {number}.\n"
    message += f"Итого - {data[0]:,}{money}.\n"
    message += f"Часы - {(data[0]-data[2]):,}{money}.\n"
    message += f"Отработано часов - {data[1]}ч.\n"

    if data[2]:
        message += f"Премия - {data[2]:,}{money}({data[3]}).\n"
    return message


async def generate_data(data: list) -> tuple:
    """Form the tuple in the correct order for the 
    subsequent generation of the message to the user.
    
    :param data: A list with data.
    """
    return data[6], data[7], data[4], data[5]


async def get_amount_and_hours_for_month(
    year: int,
    month: int,
    user_id: int,
    state: FSMContext
) -> tuple[tuple]:
    """
    Return the most necessary data for display.
    
    :param year: A year to collect information.
    :param month: A month to collect information.
    :param user_id: User ID.
    """
    total_data: tuple = await get_data_from_db(year, month, user_id)
    data: list = await data_calculation(total_data)
    
    period1: tuple[float] = (data[0][0], data[0][1])
    period2: tuple[float] = (data[1][0], data[1][1])

    await state.update_data(
        period1=data[0],
        period2=data[1],
        for_month=await generate_data(data)
    )

    return period1, period2, (data[6], data[7])
