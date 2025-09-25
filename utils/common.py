async def parse_income_expense(
    data: dict[str, str | int],
    income: bool,
    page: int
) -> tuple[str, bool, bool, str]:
    """
    Генерирует сообщение для ответа пользователю.

    :param data: Список с транзакциями.
    param income: Определяем тип транзакции.
    """
    if len(data) == 0:
        return None, 0, 0, ""

    message = f"Ваши {'доходы:' if income else 'расхлды:'}.\n"
    message += "*" * 40 + '\n'
    message += f"Дата: {str(data[page-1].get("created_at"))[:10]}.\n"
    message += f"Сумма: {'+' if income else '-'}{data[page-1]["amount"]:,}₽.\n"
    message += f"Описание: {data[page-1].get("description")}.\n"
    message += "*" * 40 + '\n\n'
    return message, len(data) > page, (page - 1) > 0, data[page-1]["_id"]
