from typing import Dict


UNICODE_DATA: Dict[int, str] = {
    1: "₁",
    2: "₂",
    3: "₃",
    4: "₄",
    5: "₅",
    6: "₆",
    7: "₇",
    8: "₈",
    9: "₉",
    10: "₁₀",
    11: "₁₁",
    12: "₁₂",
    13: "₁₃",
    14: "₁₄",
    15: "₁₅",
    16: "₁₆",
    17: "₁₇",
    18: "₁₈",
    19: "₁₉",
    20: "₂₀",
    21: "₂₁",
    22: "₂₂",
    23: "₂₃",
    24: "₂₄",
}

MONTH_DATA: Dict[int, str] = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь",
}

# Для добавления в календарь.
DAYS_LIST: tuple = ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")

start_text: str = (
    "😎 Привет! 😎 Я телеграм бот для учета рабочих "
    "смен и подсчета ожидаемой зарплаты. Чтобы узнать все мои возможности "
    "введите /info . Обязательно к прочтению!"
)

greeting: str = (
    "Рады вас видеть в нашем телеграм боте. Итак, что представляет из себя "
    "телеграм бот. Основной функционал бота это добавление и отслеживание "
    "смен в вашем рабочем графике. Давайте поговорим о всем функционале "
    "поэтапно."
)

settings: str = (
    "Первым делом вам нужно зайти в настройки и добавить свои данные по оплате "
    "труда. Они включают в себя ваша оплата труда за час и доплата "
    "за переработку. Если переработка не оплачивается то введите 0. Если "
    "этого не сделать то будут введены данные по умолчанию, и "
    "большинство функционала потеряет смысл."
)

calendar: str = (
    "Далее можно начинать пользоваться функционалом бота. Чтобы открыть "
    "календарь за текущий месяц нужно нажать на кнопку календарь в "
    "основном меню. Календарь можно листать в обе стороны(<< чтобы открыть "
    "предыдущий месяц и >> чтобы открыть следующий месяц). Чтобы добавить "
    "запись смены, нажимаем на нужное нам число календаря. Если нажать один раз "
    "то будет показано уведомление о выбранном дне, если нажать еще раз, то "
    "уже придет сообщение, либо добавить, если записей за выбранный день еще "
    "не было добавлено, либо изменить, удалить или добавить бонус если запись уже "
    "существует. Чтобы добавить запись нажимаем кнопку добавить."
    ". Бот попросит вас ввести количество отработанных часов за смену. Варианты"
    " ввода: 1) Можно вводить просто число допустим 12. Если вы задерживаетесь "
    "после основного времени и за это вам идет доплата то нужно ввести вот "
    "таким образом 9*2 где 9 это основное время, 2 это время с доплатой. Если "
    "у вас вся смена с доплатой то нужно ввести 0*9. Изменение записи повторяет "
    "добавление записи поэтому рассматривать данный вариант не будем. Если у вас"
    " какая нибудь супер акция то добавляем это как добавить бонус. Там у вам "
    "нужно будет ввести просто сумму доплаты."
)

prediction: str = (
    "Следующая кнопка прогнозирование. Прогнозирование возможно только за "
    "текущий и следующий месяца, так врят-ли кому то интересно более дальнее "
    "прогнозирование. Прогнозирование возможно для двух вариантов графика: "
    "5/2 и 2/2 так как это самые распространенные графики. Для прогнозирования "
    "5/2 вам нужно будет ввести также количество доп смен, если таковые имеются, "
    "если таковых нет то вводим 0, и количество часов которое ставиться, так "
    "как в разных организациях это делается по разному, где то вычитают обед 1ч"
    " где то ставят полностью. Далее вам будет предложено отметить все дни "
    "когда вы задерживаетесь на работе, и выбрать количество часов на которое "
    "вы задерживаетесь. Если задержки нет то ничего выбирать не нужно и просто "
    "нажимаем завершить, и вам будет показано в всплывающем уведомлении "
    "прогнозируемая зарплата. Здесь можно поиграться и повыбирать разные варианты"
    "задержек. В графике 2/2 вам так же нужно ввести количество доп смен, по "
    "сколько ставиться смена, и дополнительно нужно ввести с какого числа у "
    "вас первая смена по графику(не доп а именно смена по графику)."
)

shifts_group: str = (
    "В боте реализована возможность проставить смены сразу за несколько дней "
    "одновременно. Возможность эта как и в прогнозировании возможна только за "
    "текущий и следующий месяца. Просто отмечайте смены когда вы работаете, "
    "маленький крестик если не работаете, маленькая галочка если работаете. "
    "Затем нажимайте 'Завершить выбор', введите по сколько часов проставлять "
    "смены, и у вас придет уведомление что смены успешно проставлены, "
    "и откроется календарь."
)

finish: str = (
    "Ну вот вроде основной функционал мы рассмотрели, надеюсь работа бота не "
    "вызовет у вас сложностей. Если есть жалобы и предложения или что то где "
    "не работает, и бот просто не отвечает пишите мне /dev , попробуем все "
    "оперативно поправить."
)


add_record_text: str = (
    "Введите количество отработанных часов " "в виде. 9*2 или 9, или 12 или 6.5"
)

success_text: str = "{}\nВы заработали: {}₽"
date_pattern: str = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
unfamiliar_command: str = ("Не могу обработать ваш запрос. "
                           "\nНаиболее распространенными ошибками являются:\n"
                           "Необходимо было ввести цело число, а вы ввели "
                           "какое-то слово или не целое число. "
                           "\nНеобходимо было нажать кнопку, а вы отправили "
                           "мне какое-то сообщение.")


GUIDE: tuple = (
    greeting, settings, calendar, prediction, shifts_group, finish
)
