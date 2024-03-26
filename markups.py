from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from data import *

def main_markup() -> ReplyKeyboardMarkup:
    menu_buttons = [
        "Статистика",
        "Об эстафете ГДД",
        "Сдать сводку",
        "Коэффициенты умножения",
        "Рейтинг эстафеты",
        "Документы",
        "Регистрация в ГДД",
        "Актуальные Добрые Дела",
        "Нуждаюсь в Добром Деле",
        "Обратная связь / Ответим на вопросы"
    ]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*menu_buttons)

    return markup


def stats_markup() -> ReplyKeyboardMarkup:
    buttons = [KeyboardButton(table) for table in excel_files.keys()]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*buttons)
    markup.add(KeyboardButton("Главное меню"))
    return markup


def second_menu_markup() -> ReplyKeyboardMarkup:
    menu_buttons = [
        "Об эстафете",
        "Добрые Дела и Мероприятия",
        "Участники эстафеты",
        "Ростики. Пункты. Коэффициенты.",
        "Метрика",
        "Наглядный пример",
        "Формирование рейтингов",
        "Хештеги ГДД",
        "Техподдержка эстафеты"
    ]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*menu_buttons)
    markup.row(KeyboardButton("Главное меню"))

    return markup


def third_menu_markup() -> ReplyKeyboardMarkup:
    menu_buttons = [
        "Сводка от физ.лица (жителя)",
        "Сводка от юридичeского лица"
    ]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*menu_buttons)
    markup.row(KeyboardButton("Главное меню"))

    return markup


def third_b_menu_markup() -> ReplyKeyboardMarkup:
    menu_buttons = [
    
    ]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*menu_buttons)
    markup.row(KeyboardButton("Главное меню"))

    return markup


def fourth_menu_markup() -> ReplyKeyboardMarkup:
    menu_buttons = [
        
    ]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*menu_buttons)
    markup.row(KeyboardButton("Главное меню"))

    return markup


def fifth_menu_markup() -> ReplyKeyboardMarkup:
    menu_buttons = [
        
    ]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*menu_buttons)
    markup.row(KeyboardButton("Главное меню"))

    return markup


def sixth_menu_markup() -> ReplyKeyboardMarkup:
    menu_buttons = [
       "Указ Губернатора Ростовской области",
       "Проект эстафеты Года Добрых Дел",
    ]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*menu_buttons)
    markup.row(KeyboardButton("Главное меню"))

    return markup


def seventh_menu_markup() -> ReplyKeyboardMarkup:
    menu_buttons = [
        "Юридическое лицо",
        "Физическое лицо",
        
    ]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*menu_buttons)
    markup.row(KeyboardButton("Главное меню"))

    return markup


def eighth_menu_markup() -> ReplyKeyboardMarkup:
    menu_buttons = [
        
    ]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*menu_buttons)
    markup.row(KeyboardButton("Главное меню"))

    return markup


def ninth_menu_markup() -> ReplyKeyboardMarkup:
    menu_buttons = [
        
    ]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*menu_buttons)
    markup.row(KeyboardButton("Главное меню"))

    return markup


def tenth_menu_markup() -> ReplyKeyboardMarkup:
    menu_buttons = [
        
    ]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*menu_buttons)
    markup.row(KeyboardButton("Главное меню"))

    return markup


def tables_markup() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(table, callback_data=f"upload_table {i}") 
        for i, table in enumerate(excel_files.keys())
    ]
    markup = InlineKeyboardMarkup()
    markup.add(*buttons)
    return markup