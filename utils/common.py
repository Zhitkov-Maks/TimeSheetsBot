from datetime import datetime

from utils.calculate import calc_valute
from utils.valute import get_valute_info


async def parse_income_expense(
    data: dict[str, str | int],
    income: bool,
    page: int
) -> tuple[str, bool, bool, str]:
    """
    Generate a message to reply to the user.

    :param data: A list with transactions.
    :param income: Defining the transaction type.
    """
    if len(data) == 0:
        return None, 0, 0, ""

    message = f"Ваши {'доходы:' if income else 'расхлды:'}.\n"
    message += "*" * 40 + '\n'
    message += f"Дата: {str(data[page-1].get("date"))[:7]}.\n"
    message += f"Сумма: {'+' if income else '-'}{data[page-1]["amount"]:,}₽.\n"
    message += f"Описание: {data[page-1].get("description")}.\n"
    message += "*" * 40 + '\n\n'
    return message, len(data) > page, (page - 1) > 0, data[page-1]["_id"]


async def calculation_currency(amount: float) -> dict:
    """
    Calculate the amount in the currency.
    
    :param amount: The amount to convert.
    """
    currency_info: dict = await get_valute_info()
    return await calc_valute(amount, currency_info)
