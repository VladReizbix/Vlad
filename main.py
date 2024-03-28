from contextlib import suppress
import os
import pandas as pd
from telebot import TeleBot
from telebot.types import Message, CallbackQuery
import json
from markups import *
from data import *
import logging
from datetime import datetime


bot = TeleBot('7016625283:AAG7oNk9FoQDKC8_xqRc-tsE-0S83Wm9xXk', parse_mode="Markdown")
ADMINS = [897929245]
documents = {}
log_chat_id = '-1002112436208'
table_requests_count = {}
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.basicConfig(filename='bot.log', level=logging.INFO)


messages = {
    "Главное меню": {"text": "{user} выбери нужный пункт меню!", "markup": main_markup()},
    "Статистика": {"text": "Я могу помочь вам с информацией. Нажмите на одну из кнопок ниже.","photo": "./Статистика.PNG", "markup": stats_markup()},
    
    "Об эстафете ГДД": {"text": "Выберите в меню нужный пункт👇", "photo": "./Штепа.PNG", "markup": second_menu_markup()},
    "Об эстафете": {"text": "*Эстафета Год Добрых Дел* – это уникальная инициатива, которая способствует укреплению социальной ответственности среди жителей, организаций и муниципальных образований.\n\nКаждый участник, будь то обычный гражданин или целая организация, стремится внести свой вклад в общее благо *путем выполнения добрых дел*, которые, в свою очередь, оцениваются в Ростиках.\n\nЭти действия не просто улучшают наш регион, но и позволяют участникам соревноваться в благотворительности, тем самым стимулируя их к еще более активному участию.\n\nСистема начисления Ростиков в эстафете выстроена таким образом, что учитывает различия в возможностях участников.\n\nЖители небольших городов и сел имеют шанс конкурировать на равных *благодаря коэффициентам*, которые компенсируют разницу в населении.\n\nТак, муниципальные образования также *становятся участниками рейтинга*, что позволяет оценить их достижения в рамках проделанной работы.\n\nВ ходе эстафеты ведется подсчет мероприятий, добрых дел у всех участников, а участники с наибольшим их количеством *получают заслуженные награды* в различных номинациях.\n\nЗа каждое совершенное доброе дело житель *получает 10 Ростиков*, которые умножаются на коэффициент территориального образования в чьих границах совершен добрый поступок.\n\nКоличество начисленных Ростиков и свою *статистику жители* могут узнать в телеграм боте эстафеты - *@GDD_RO_bot*.\n\nНаграждаются не только индивидуальные исполнители, но и организации, которые ранжируются в категориях по размеру и типу деятельности для формирования объективного рейтинга.\n\nЭти награды служат не только признанием заслуг, но и мощным стимулом для продолжения добровольческой активности, распространения идеи добрых дел в широких массах и укрепления социальных связей внутри региона." },
    "Добрые Дела и Мероприятия": {"text": "В рамках представленной игровой системы - эстафеты выделяют два дискретных понятия:\n*«Доброе дело»* и *«Мероприятие»*.\n*«Доброе дело»* – это акция, совершенная одним конкретным жителем, а *«Мероприятие»* – это комплекс организованных добрых дел, совершенных в одно и тоже время,открытых надсубъектом.\n\n*Например:* Министерство ЖКХ, которое является над субъектом в игровой системе, в городе Таганроге решило провести субботник силами своих сотрудников. Оно создает одно мероприятие, посвященное данному субботнику, на которое пригласило 10 человек из своего штата. Каждый из участников субботника сделал свое одно доброе дело: убрал листья с дороги, выкинул мусор, посадил дерево. Следовательно, в рамках мероприятия субботника совершенно 10 добрых дел по количеству приглашенных участников.Жители небольших городов и сел имеют конкурировать на равных благодаря коэффициентам, которые компенсируют разницу в населении.", "photo": "./Добрые Дела.PNG"},
    "Участники эстафеты": {"text": "1.*Жители Ростовской области*, физические лица.\n\n2.*Юридические лица* следующих видов:\n\n✅НКО\n\n✅Бизнес\n\n✅РОИВ\n\n✅Образовательные учреждения\n\n3.*Муниципальные образования*.\n\n*РОИВ* представлены 31 организациями,которые включают в себя министерства, департаменты, комитеты, управления, инспекции и службы.\n\n*Муниципальных образований в Ростовской области* - их строго 55, тогда как список остальных над субъектов формируется открытым способом по мере их регистрации в системе.", "photo": "./УчастникиЭстафеты.PNG",},
    "Ростики. Пункты. Коэффициенты.": {"text": "За каждое выполненное доброе дело житель получает фиксированное количество Ростиков (игровых очков, которые можно обменять на призы), а именно 10, которые перемножаются на коэффициент того глобального субъекта (города и т.д.), на территории которого совершалось доброе дело.\n\nКаждое муниципальное образование имеет свой коэффициент активности от 1.0 до 2.0, на который перемножаются Ростики жителя, совершившего доброе дело на данной территории.\n\nЕсли житель совершил доброе дело на территории муниципального образования, у которого, коэффициент умножения 1.5, то жителю начислят 10 Ростиков за доброе дело, которые потом будут умножены на коэффициент 1.5 (в данном случае 1.5) и в итоге он получит 15 Ростиков.\n\nКоэффициент умножения муниципального образования увеличивается по мере выполнения добрых дел всеми жителями.При этом требования к каждому муниципальному образованию зависят от количества проживающих в нем граждан.\n\n*Например:* В г. Ростове-на-Дону проживает 1 135 968 жителей и для того, чтобы коэффициент умножения увеличивался на 0.1 жителям необходимо выполнить 1136 добрыхдела для следующего повышения, а вот в г. Новошахтинске проживает 101 708 жителей и для того, чтобы коэффициент умножения увеличивался на 0.1 жителям необходимо выполнять по 102 добрых дела для следующего повышения.\n*Алгоритм расчёта:* разделить на количество людей, проживающих на территории муниципального образования на 1000, округляя в большую сторону, и по достижении порога данного числа повышать рейтинг муниципального образования на 0,1. Такой подход создает условия для мотивации жителей к сплочению в ходе эстафеты.\n\nТекущие коэффициенты муниципальных образований в панель коэффициентов."},
    "Метрика.": {"text": "Учет проведенных добрых дел и мероприятий формируется по следующим правилам:\n\n✅Для жителей учитывается *совершенные ими добрые дела* и ведется подсчет Ростиков.\n\n✅Для организаций учитываются как организованные ими *мероприятия*, так и совершенные жителями в их рамках *добрые дела*.\n\n✅Если житель выполнил доброе дело *по своей инициативе* без организации надсубъектов, тогда данное доброе дело идет только в его рейтинг и в рейтинг глобального субъекта.\n\n✅В рейтинг глобальных субъектов *идет каждое совершенное* доброе дело и мероприятия на его территории.", "photo": "./Наглядный.PNG"},
    "Наглядный пример": {"text": "*Пример №1* - Министерство транспорта (Орган власти Ростовской области) организовало в Ростове-на-Дону общественную выставку современных транспортных средств, в которой приняли участие волонтеры Артур и Ольга.Они помогали в организации процесса вместе с более 100 жителями, любовавшимися транспортом.\n\n*Как производится расчет?*\n\nСмотрим коэффициенты города Ростов-на-Дону (1.3).\n\n*Результат:*\n\n*•Министерство транспорта получает в свою статистику:* 1 Мероприятие.\n\n*•Артур получает в свою статистику:* 1 Доброе Дело, 13 Ростиков (из расчета 10 х 1.3).\n\n*•Ольга получает в свою статистику:* 1 Доброе Дело, 13 Ростиков (из расчета 10 х 1.3).\n\n*•Ростов-на-Дону получает в свою статистику:* 1 Мероприятие, 2 Добрых Дела.\n\n*Пример №2* - Таганрогская организация ЦМЛ Движение вверх организовала в Ростове-на-Дону мастер - класс по плетению маскировочных сетей, на которое приехали волонтеры Аня и Алина из Таганрога, а ещё пришёл Кирилл из Ростова-на-Дону.\n\n*Как производится расчет?*\n\nСмотрим коэффициенты городов, например в Таганроге действует коэффициент 1.7, а в Ростове-на-Дону 1.3.\n\n*Результат:*\n\n*Организация ЦМЛ получает в метрику* - 1 Мероприятие.\n\n*•Аня получает в свою статистику:* 1 Доброе Дело, 13 Ростиков (из расчета 10 х 1.3).\n\n*•Алина получает в свою статистику:* 1 Доброе Дело, 13 Ростиков (из расчета 10 х 1.3).\n\n*•Кирилл получает в свою статистику:* 1 Доброе Дело, 13 Ростиков (из расчета 10 х 1.3).\n\n*•Ростов-на-Дону получает в свою статистику:* 1 Мероприятие, 3 Добрых Дела.Как мы видим, к Ане и Алине применяется коэффициент Ростова-на-Дону, несмотря на то, что они из Таганрога.\n\nУчитывается территориальность самого доброго дела, а не место регистрации участника.\n\nВсе показатели засчитываются Ростову-на-Дону, несмотря на то, что в нем принимали участие волонтеры из Таганрога."},
    "Формирование рейтингов.": {"text": "В конце эстафеты *«Год Добрых Дел»* будет объявлен список *«ТОП самых добрых жителей Ростовской области»*, в котором будут лица, совершившие наибольшее количество добрых дел.\n\nТак же в завершение года будет реализована призовая программа, по принципу которой Ростики, полученные жителями за добрые дела, можно будет обменять на ценные призы. Список призов и их оценка в Ростиках будут опубликованы в ходе эстафеты дополнительно.\n\nВсе организации формируют рейтинг по своим категориям в двух номинациях: по организованным мероприятиям и по совершенным в рамках мероприятий добрым делам.\n\n*Рейтинг рассчитывается следующим образом:\n\n*1.*Некоммерческие организации*. В зависимости от количества активных волонтеров, все Некоммерческие организации делятся на две группы – крупные (от 750 волонтеров на ДОБРО.РФ) и средние (до 750 волонтеров). В рамках данных групп формируется рейтинг участников как по количеству организованных мероприятий, так и по количеству проведенных добрых дел в рамках мероприятий.\n\n2.*Бизнес*. В зависимости от количества сотрудников в штате, бизнес организации поделены на три категории: малый бизнес (от 1 до 16 сотрудников), средний бизнес (16 - 250) и крупный бизнес (251 и более). В рамках данных групп формируется рейтинг участников, как по количеству организованных мероприятий, так и по количеству проведенных добрых дел в рамках своих мероприятий.\n\n3.*Органы власти Ростовской области*. Рейтинг данного типа участников формируется в зависимости от количества организованных мероприятий и проведенных добрых дел.\n\n4.*Образовательные учреждения*. В рамках эстафеты выделяют три группы образовательных учреждений: Общеобразовательные учреждения, Профессиональные образовательные учреждения и Образовательные организации высшего образования.\n\nВ рамках данных групп рейтинг мероприятий формируется исходя из следующей формулы:1 делить на X умножить на М\nГде X – количество учащихся.\nМ - количество проведенных мероприятий.\n\nРейтинг добрых дел формируется по аналогичному принципу.\n\nВ конце года будут подведены итоги и будут определены и награждены лучшие в своих категориях."},
    "Хештеги ГДД": {"text": "*#донволонтер* *#донмолодой* *#годдобрыхдел* *#бытьдобрунадону*", "photo": "./Красные.PNG"},
    "Техподдержка эстафеты": {"text": "Техподдержка по вопросам работы эстафеты с 10:00 до 20:00 часов ежедневно по номеру *+7-989-552-61-75*.\n\nМы с радостью ответим на ваши вопросы, но изначально рекомендуем ознакомиться со всеми правилами работы эстафеты Года Добрых Дел.", "photo": "./Держит ГДД.PNG"},

    "Сдать сводку": {"text": "Выберете в меню от кого вы желаете сдать сводку👇", "markup": third_menu_markup()},
    "Сводка от физ.лица (жителя)": {"text": "[Сводка от физ.лица (жителя)](https://clck.ru/39Gx78)", "photo": "./для физ лиц.PNG"},
    "Сводка от юридичeского лица": {"text": "[Сводка от юридичeского лица](https://clck.ru/39Gx95)", "photo": "./Алгоритм.PNG", "markup": third_b_menu_markup()},
    "РОИВ": {"text": "[РОИВ](https://clck.ru/39GxAG)"},
    "НКО": {"text": "[НКО](https://clck.ru/39GxAo)"},
    "БИЗНЕС": {"text": "[БИЗНЕС](https://clck.ru/39GxCo)"},
    "ОБРАЗОВАНИЕ": {"text": "[ОБРАЗОВАНИЕ](https://clck.ru/39GxEW)"},

    "Коэффициенты умножения": {"text": "[Коэффициенты умножения муниципальных образований](https://clck.ru/39QoNo)","photo": "./коэфф.PNG", "markup": fourth_menu_markup()},
    "Рейтинг эстафеты": {"text": "[Рейтинг эстафеты](https://clck.ru/39KG32)","photo": "./Алина.PNG", "markup": fifth_menu_markup()},
    "Документы": {"text": "Выберете в меню какой документ хочешь посмотреть:👇", "photo": "./Леша.PNG", "markup": sixth_menu_markup()},
    "Указ Губернатора Ростовской области": {"text": "[Указ Губернатора Ростовской области](https://www.donland.ru/documents/18634/)"},
    "Проект эстафеты Года Добрых Дел": {"text": "[Проект эстафеты Года Добрых Дел]()"},

    "Регистрация в ГДД": {"text": "Выберете в меню в качестве кого вы хотите зарегистрироваться в эстафете👇", "photo": "./Регистрация ГДД.PNG", "markup": seventh_menu_markup()},
    "Юридическое лицо": {"text": "[Регистрация для юридических лиц](https://clck.ru/39GxMU)"},
    "Физическое лицо": {"text": "[Регистрация для физических лиц](https://clck.ru/39GxNU)"},
    

    "Актуальные Добрые Дела": {"text": "[Актуальные Добрые Дела](https://clck.ru/39GxPU)","photo": "./пацан с маленькой.PNG" , "markup": eighth_menu_markup()},
    "Нуждаюсь в Добром Деле": {"text": "Если вам требуется помощь волонтеров, то вы можете обратиться в техническую поддержку эстафеты *Года Добрых Дел*, и мы вам обязательно поможем!🙂\n*Техподдержка эстафеты работает с 10:00 до 20:00 часов ежедневно по номеру:*\n*+7-989-552-61-75*\n*ТГ аккаунт*:@goddobryhdel\n*Электронная почта*:\ngoddobryhdel@yandex.ru\n", "photo": "./Девушка с шариками.PNG", "markup": ninth_menu_markup()},
    "Обратная связь / Ответим на вопросы": {"text": "Напишите нам в личные сообщения, мы постараемся вам ответить в самое ближайшее время! Наш график работы с 10:00 до 20:00 часов ежедневно, без выходных.\n*ТГ аккаунт*:@goddobryhdel\n*Электронная почта*:\ngoddobryhdel@yandex.ru\n", "photo": "./В белых вещах пацан и девка.PNG","markup": tenth_menu_markup()},
}

def save_message_id(message_id: int) -> None:
    with open("message_ids.txt", "a") as file:
        file.write(f"{message_id}\n")

try:
    with open('request_counts.json', 'r') as file:
        request_counts_data = json.load(file)
except FileNotFoundError:
    request_counts_data = {'table_requests_count': {}, 'total_requests': 0, 'dates': {}}


def save_request_counts():
    with open('request_counts.json', 'w') as file:
        json.dump(request_counts_data, file)


def send_text_and_photo_to_group(message, photo_path):
    with open(photo_path, 'rb') as photo:
        bot.send_photo(chat_id=log_chat_id, photo=photo, caption=message)  


def get_text(row, table_name, chat_id):
    now = datetime.now()  

    if table_name in request_counts_data['table_requests_count']:
        request_counts_data['table_requests_count'][table_name] += 1
    else:
        request_counts_data['table_requests_count'][table_name] = 1
    request_counts_data['total_requests'] += 1

    
    if table_name in request_counts_data['dates']:
        request_counts_data['dates'][table_name].append(now.isoformat())
    else:
        request_counts_data['dates'][table_name] = [now.isoformat()]

    formatted_date = now.strftime("%d-%m-%Y") 

    log_message = (
        f"Таблица: {table_name}\n"
        f"Общее количество запросов для таблицы: {request_counts_data['table_requests_count'][table_name]}\n"
        f"Общее количество запросов: {request_counts_data['total_requests']}\n"
        f"Дата: {formatted_date}"
    )
    photo_path = None  

    
    if table_name == 'Житель':
        photo_path = './логологи.jpg'  
    elif table_name == 'НКО':
        photo_path = './логологи.jpg'  
    elif table_name == 'РОИВ':
        photo_path = './логологи.jpg'  
    elif table_name == 'Бизнес':
        photo_path = './логологи.jpg'  
    elif table_name == 'Школа':
        photo_path = './логологи.jpg'  
    elif table_name == 'Колледж':
        photo_path = './логологи.jpg'  
    elif table_name == 'ВУЗ':
        photo_path = './логологи.jpg'  

   
    send_text_and_photo_to_group(log_message, photo_path)

    
    save_request_counts()

    match table_name:
        case 'Житель': 
            photo_path = './1л.jpg'  
            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo)
            return (
                f"*ID жителя:* {int(row['ID'].values[0])}\n"
                f"ФИО: {row['ФИО'].values[0]}\n"
                f"Общее количество добрых дел: {int(row['Общее количество Добрых Дел'].fillna(0).values[0])}\n"
                f"Общее количество Ростиков: {int(row['Общее количество Ростиков'].fillna(0).values[0])}\n"
                f"Город: {row['Глобальный субъект'].values[0]}\n"
                f"Текущий коэффициент: {int(row['Текущий коэффициент'].fillna(0).values[0])}\n"
                f"Личный Рейтинг: {int(row['Рейтинг'].fillna(0).values[0])}\n"
            )
        case 'НКО':
            photo_path = './2л.jpg'  
            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo)
            return (
                f"*ID организаций:* {int(row['ID'].values[0])}\n"
                f"Название организаций: {row['Название организации'].values[0]}\n"
                f"Тип НКО: {row['Тип НКО'].values[0]}\n"
                f"Общее количество выполненных мероприятий: {int(row['Общее количество Мероприятий'].fillna(0).values[0])}\n"
                f"Общее количество добрых дел: {int(row['Общее количество Добрых дел'].fillna(0).values[0])}\n"
                f"Город: {row['Глобальный субъект'].values[0]}\n"
                f"Личный рейтинг: {int(row['Рейтинг'].fillna(0).values[0])}\n"
            )
        case 'РОИВ':
            photo_path = './3л.jpg'  
            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo)
            return (
                f"*ID организаций:* {int(row['ID'].values[0])}\n"
                f"Название организаций: {row['Название организации'].values[0]}\n"
                f"Общее количество выполненных мероприятий: {int(row['Общее количество Мероприятий'].fillna(0).values[0])}\n"
                f"Общее количество добрых дел: {int(row['Общее количество Добрых дел'].fillna(0).values[0])}\n"
                f"Мероприятия в категории: Иное {int(row['Мероприятия в категории: Иное'].fillna(0).values[0])}\n"
                f"Личный рейтинг: {int(row['Рейтинг'].fillna(0).values[0])}\n"
            )
        case 'Бизнес':
            photo_path = './4л.jpg'
            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo)
            return (
                f"*ID организации:* {int(row['ID'].values[0])}\n"
                f"Название организаций: {row['Название организации'].values[0]}\n"
                f"Штат: {row['Штат'].values[0]}\n"
                f"Тип бизнеса: {row['Тип бизнеса'].values[0]}\n"
                f"Общее количество выполненных мероприятий: {int(row['Общее количество Мероприятий'].fillna(0).values[0])}\n"
                f"Общее количество добрых дел: {int(row['Общее количество Добрых дел'].fillna(0).values[0])}\n"
                f"Город: {row['Глобальный субъект'].values[0]}\n"
                f"Личный рейтинг: {int(row['Рейтинг'].fillna(0).values[0])}\n"
            )

        case 'Школа':
            photo_path = './5л.jpg'
            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo)
            return (
                f"*ID организации:* {int(row['ID'].values[0])}\n"
                f"Название организаций: {row['Название организации'].values[0]}\n"
                f"Общее количество выполненных мероприятий: {int(row['Общее количество Мероприятий'].fillna(0).values[0])}\n"
                f"Общее количество активных участников на мероприятиях: {int(row['Общее количество Добрых дел'].fillna(0).values[0])}\n"
                f"Город: {row['Глобальный субъект'].values[0]}\n"
                f"Личный рейтинг: {int(row['Рейтинг'].fillna(0).values[0])}\n"
            )

        case 'Колледж':
            photo_path = './6л.jpg'
            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo)
            return (
                f"*ID организации:* {int(row['ID'].values[0])}\n"
                f"Название организаций: {row['Название организации'].values[0]}\n"
                f"Общее количество выполненных мероприятий: {int(row['Общее количество Мероприятий'].fillna(0).values[0])}\n"
                f"Общее количество активных участников на мероприятиях: {int(row['Общее количество Добрых дел'].fillna(0).values[0])}\n"
                f"Город: {row['Глобальный субъект'].values[0]}\n"
                f"Личный рейтинг: {int(row['Рейтинг'].fillna(0).values[0])}\n"
            )

        case 'ВУЗ':
            photo_path = './4л.jpg'
            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo)
            return (
                f"*ID организации:* {int(row['ID'].values[0])}\n"
                f"Название организаций: {row['Название организации'].values[0]}\n"
                f"Общее количество выполненных мероприятий: {int(row['Общее количество Мероприятий'].fillna(0).values[0])}\n"
                f"Общее количество активных участников на мероприятиях: {int(row['Общее количество Добрых дел'].fillna(0).values[0])}\n"
                f"Город: {row['Глобальный субъект'].values[0]}\n"
                f"Личный рейтинг: {int(row['Рейтинг'].fillna(0).values[0])}\n"
            )
        case _:
            return "Таблица не найдена"


def process_query(message: Message, table: str) -> None:
    temporary_message = bot.send_message(message.chat.id, "Выполняю поиск...")
    markup = stats_markup()

    name = message.text.strip()
    if not name.isdigit():
        bot.delete_message(message.chat.id, temporary_message.message_id)
        return bot.send_message(
            message.chat.id, 
            f"ID \"{name}\" должен быть числом, попробуйте ввести другое значение.",
            reply_markup=markup
        )

    file_name = excel_files.get(table) 
    if file_name:  
        try:
            df = pd.read_excel(file_name)
            row = df[df['ID'] == int(name)]
            if not row.empty:
                text = get_text(row, table, message.chat.id)  
                bot.send_message(message.chat.id, text, reply_markup=markup)
            else:
                bot.send_message(
                    message.chat.id, 
                    f"Данный запрос \"{message.text}\" не найден в системе, попробуйте ввести другое ID.",
                    reply_markup=markup
                )
            bot.delete_message(message.chat.id, temporary_message.message_id)
        except Exception as e:
            bot.send_message(
                message.chat.id, 
                f"Ошибка при выполнении запроса из базы данных: {e}",
                reply_markup=markup
            )
            bot.delete_message(message.chat.id, temporary_message.message_id)
    else:
        result = "Таблица не найдена"
        if isinstance(result, str):
            bot.delete_message(message.chat.id, temporary_message.message_id)
            sended_message = bot.send_message(message.chat.id, result, reply_markup=markup)
            save_message_id(sended_message.message_id)  
        else:
            bot.delete_message(message.chat.id, temporary_message.message_id)
            bot.send_message(message.chat.id, "Ошибка при выполнении запроса", reply_markup=markup)

bot.send_message(log_chat_id,'Бот запущен')


@bot.message_handler(commands=['start'])
def send_welcome(message: Message) -> None:
    markup = main_markup()
    with open('Сердечко.PNG', 'rb') as photo_file:
        bot.send_photo(message.chat.id, photo_file, caption=f"Приветствую, {message.from_user.first_name}! Я телеграмм бот эстафеты и буду тебе помогать в течение всего года!\n\nВыбери нужный пункт меню!👇", reply_markup=markup)
    
   
    bot.send_message(log_chat_id, f'Команда /start обработана. Пользователь: {message.from_user.id}, Имя: {message.from_user.first_name}')

@bot.message_handler(func=lambda message: message.text and message.text in excel_files)
def handle_button(message: Message) -> None:
    msg = bot.send_message(message.chat.id, f"Вы выбрали \"{message.text}\". Введите ID:")
    bot.register_next_step_handler(msg, process_query, table=message.text)


@bot.message_handler(func=lambda message: message.text and message.text in messages)
def handle_menu(message: Message) -> None:
    data = messages[message.text]
    text= data.get("text")
    if text:
     text = text.format(user = message.from_user.first_name)
    markup = data.get("markup")
    photo = data.get("photo")
    video = data.get("video")
    document = data.get("document")
    if photo:
        with open(photo, 'rb') as photo_file:
            bot.send_photo(message.chat.id, photo_file, caption=text, reply_markup=markup)
    elif video:
        with open(video, 'rb') as video_file:
            bot.send_video(message.chat.id, video_file, caption=text, reply_markup=markup)
    elif document:
        with open(document, 'rb') as document_file:
            bot.send_document(message.chat.id, document_file, caption=text, reply_markup=markup)
    elif text:
        bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(content_types=['document'])
def handle_table(message: Message) -> None:
    if message.from_user.id not in ADMINS:
        return
    
    documents[message.chat.id] = message.document.file_id
    bot.send_message(
        message.chat.id, 
        "Выберите таблицу, которую хотите загрузить:",
        reply_markup=tables_markup()
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("upload_table "))
def upload_table(callback_query: CallbackQuery) -> None:
    if callback_query.from_user.id not in ADMINS:
        return
    
    table_index = int(callback_query.data.split()[1])
    table_path = list(excel_files.values())[table_index]
    file_id = documents.get(callback_query.message.chat.id)
    if file_id is None:
        return bot.edit_message_text(
            "Файл не найден, попробуйте еще раз.",
            callback_query.message.chat.id,
            callback_query.message.message_id
        )

    file_info = bot.get_file(file_id)
    file = bot.download_file(file_info.file_path)
    
    with suppress(FileNotFoundError):
        os.remove(table_path)
    with open(table_path, 'wb') as new_file:
        new_file.write(file)
    
    bot.edit_message_text(
        f"Таблица \"{table_path}\" успешно загружена.",
        callback_query.message.chat.id,
        callback_query.message.message_id
    )
    del documents[callback_query.message.chat.id]



if __name__ == "__main__":
    bot.polling()
