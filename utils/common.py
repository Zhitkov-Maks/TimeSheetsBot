async def parse_income_expense(
    data: dict[str, str | int], income: bool
) -> str:
    """
    Генерирует сообщение для ответа пользователю.
    
    :param data: Список с транзакциями.
    param income: Определяем тип транзакции.
    """
    if len(data) == 0:
        return "Записей не найдено."
    
    message = f"Ваши {'доходы:' if income else 'расхлды:'}.\n"
    for item in data:
        message += "*" * 40 + '\n'
        message += f"Дата: {str(item.get("created_at"))[:10]}.\n"
        message += f"Сумма: {'+' if income else '-'}{item["amount"]:,}₽.\n"
        message += f"Описание: {item.get("description")}.\n"
        message += "*" * 40 + '\n\n'
    return message
