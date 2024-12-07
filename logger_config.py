import logging
from logging.handlers import RotatingFileHandler


bot_logger = logging.getLogger("bot_logger")
bot_logger.setLevel(logging.INFO)


# Создание обработчика для записи логов в файл с ротацией
file_handler = RotatingFileHandler(
    "./logs/error_log.txt",
    maxBytes=5*1024*1024,  # Ограничение размера файла 5 МБ
    backupCount=3  # Хранить 3 резервные копии
)
file_handler.setLevel(logging.ERROR)

# Создание обработчика для вывода логов в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Форматирование сообщений
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

bot_logger.addHandler(file_handler)
bot_logger.addHandler(console_handler)
