import calendar


async def generate_message_statistic(
    for_hours: dict, for_other: dict, year: int
) -> str:
    """Сгенерируй сообщение для пользователя."""
    if len(for_hours) == 0:
        return "Информации за выбранный год нет!"

    earned, hours = (
        for_hours.get("total_earned", 0), for_hours.get("total_hours", 0)
    )
    other_earned = for_other.get("total_other_amount", 0)
    days = 366 if calendar.isleap(year) else 365

    message = "*" * 40 + "\n\n"
    message += f"Некоторая статистика за {year} год.\n\n"
    message += f"Всего отработано часов: {hours}ч.\n"
    message += f"То есть вы провели на работе {round(hours / 24, 1)} дней.\n"
    message += f"Или {round((hours) / (days * 24) * 100, 1)}% времени в году.\n"
    message += f"Вы заработали: {(earned + other_earned):,}₽.\n\n"
    message += "*" * 40 + "\n\n"

    return message
