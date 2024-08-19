from datetime import datetime

from aiogram.types import KeyboardButton

start_text = (
    "😎 Привет! 😎 Я телеграм бот для удобного "
    "подсчета зарплаты оператора штабелера. "
    "Чтобы узнать больше нажмите /help."
)

guide = (
    """
Бот поможет отслеживать вашу зарплату.
Просто заносите данные каждый отработанный 
день, и бот будет считать все за вас.
В первую очередь необходимо указать
стоимость вашего часа и прибавку к 
часу который считается переработкой,
так как по умолчанию бот будет считать 
300 и 100, соответственно. Сделать 
это можно нажав на кнопку меню, и 
выбрать /settings. Теперь можно 
добавить запись. Чтобы добавить 
запись за текущий день, достаточно 
просто нажать сегодня, дальше бот 
попросит вас ввести часы. 
Примеры ввода:
9 - Отработана смена 9 часов без
доп надбавки.
9*2 - отработано 9 часов по обычной 
ставке и два часа с доплатой.
0*9 - Смена была полностью с доп надбавкой.
Не целые числа тоже допускаются,
например выглядеть будет так 9.5*2, 
обязательно должна быть точка, иначе
данные не примутся. 
Если хотите за другое число добавить 
запись, то нажмите на добавить доход.
Выберите число, и занесите часы.
Посмотреть информацию о вашем доходе
нажав на текущий месяц. 
""")

add_record_text = ("Введите количество отработанных часов "
                   "в виде. 9*2 или 9, или 12 или 6.5")

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

reset_to_zero = [
    [KeyboardButton(text="Да"), KeyboardButton(text="Нет")]
]


success_text = "Супер!!!\n{} - вы заработали\n 💰💰💰💵💵💵 -> {}₽"
