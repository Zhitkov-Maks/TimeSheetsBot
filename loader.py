from datetime import datetime

from aiogram.types import KeyboardButton

start_text = (
    "😎 Привет! 😎 Я телеграм бот для удобного "
    "подсчета зарплаты оператора штабелера. "
    "Чтобы вызвать меню введите /help ."
)

guide = (
    """
В первую очередь необходимо указать
стоимость вашего часа и прибавку к 
часу который считается переработкой,
так как по умолчанию бот будет считать 
300 и 100, соответственно. Часы при 
добавлении записи нужно писать целым 
числом, иначе бот неправильно будет
считать(пока только так, в будущем 
возможно обдумаем как это лучше 
реализовать, тут есть сложность с 
проверкой введенных данных).
""")

add_record_text = ("Введите количество отработанных часов. "
                   "Например, если вы отработали 9 часов "
                   "и они без доп надбавок то введите "
                   "просто 9, если например вы отработали "
                   "11 часов из них 2 часа с надбавкой то"
                   "введите 9*2, если вся смена с надбавкой "
                   "то введите 0*9. Не целые числа пока не "
                   "допускаются.")

year_list = [
    [
        KeyboardButton(text=str(datetime.now().year - 2)),
        KeyboardButton(text=str(datetime.now().year - 1)),
        KeyboardButton(text=str(datetime.now().year)),
    ]
]

month_list = [
    [
        KeyboardButton(text="Январь"),
        KeyboardButton(text="Февраль"),
        KeyboardButton(text="Март"),
        KeyboardButton(text="Апрель"),
    ],
    [
        KeyboardButton(text="Май"),
        KeyboardButton(text="Июнь"),
        KeyboardButton(text="Июль"),
        KeyboardButton(text="Август")
    ],
    [
        KeyboardButton(text="Сентябрь"),
        KeyboardButton(text="Октябрь"),
        KeyboardButton(text="Ноябрь"),
        KeyboardButton(text="Декабрь")
    ]
]

select_keyboard = [
    [KeyboardButton(text="Да"), KeyboardButton(text="Нет")]
]
