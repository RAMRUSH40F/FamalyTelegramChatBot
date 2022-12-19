import datetime
import os
import time

import telebot
from telebot import types

from Famaly_chat_Telegram_bot.src.BinApi import ShoppingList
from Famaly_chat_Telegram_bot.src.Weather_api import Weather
from config import token, starting_message

bot = telebot.TeleBot(token)


# This is a main tree of received message.
# Функция перераспределяет запросы пользователей по функциям.
# Telegram.message object -> void
def message_handler(message):
    #  ГЛАВНОЕ МЕНЮ
    if message.text in ['меню', 'Меню', '@renatakamilabot', 'Старт', 'старт', 'Начать', 'начать', 'Привет', 'привет',
                        'Назад']:
        # bot.send_message(message.chat.id,message.chat.id)
        # bot.send_message(message.chat.id, message.json['from']['first_name'])
        show_main_menu(message)

    #  WEATHER SECTION
    #  Послать погоду на сегодня
    elif message.text in ['Погода', "погода"]:
        get_weather(message.chat.id)

    #  FOODSTUFF LIST SECTION
    #  Раздел списка продуктов
    elif message.text in ['Список Продуктов', 'Посмотреть список продуктов', 'Добавить продукты', 'Очистить']:
        if message.text == 'Список Продуктов':
            show_shopping_menu(message)
        elif message.text == 'Посмотреть список продуктов':
            get_shopping_list(message)
        elif message.text == 'Добавить продукты':
            shoplist_update_handler(message)
        elif message.text == 'Очистить':
            ShoppingList.delete(message.chat.id)

    # WORD CENSORSHIP SECTION
    #  Модерируем плохие слова .
    elif contains_bad_words(message.text):
        bot.delete_message(message.chat.id, message.id)


# This gives a user a main menu section buttons
# Telegram.message object -> void
def show_main_menu(message):
    menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_weather = types.KeyboardButton(text='Погода')
    btn_store_list = types.KeyboardButton(text='Список Продуктов')
    menu.add(btn_store_list, btn_weather)
    bot.send_message(message.chat.id, 'Вот список моих функций на сегодня. Пользуйся :) ', reply_markup=menu)


# These funcs gives a user a FOODSTUFF section buttons
# Telegram.message object -> void
def show_shopping_menu(message):
    bot.delete_message(message.chat.id, message.id)
    btn_back = types.KeyboardButton(text='Назад')
    btn_show_shopping_list = types.KeyboardButton(text='Посмотреть список продуктов')
    btn_add_to_shopping_list = types.KeyboardButton(text='Добавить продукты')

    shopping_menue = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    shopping_menue.add(btn_back, btn_show_shopping_list, btn_add_to_shopping_list)
    bot.send_message(message.chat.id, 'Ты можешь посмотреть или добавить в список продуктов ',
                     reply_markup=shopping_menue)


# shopping list button
# Telegram.message object -> void
def get_shopping_list(message):
    bot.delete_message(message.chat.id, message.id)
    bot.send_message(message.chat.id, '<b>Текущий список покупок:</b>', parse_mode='HTML')
    bot.send_message(message.chat.id, ', '.join(ShoppingList.get()))


# Telegram.message object -> void
def shoplist_update_handler(message):
    reccomendation_text = 'В следующем предложении ты можешь написать ' \
                          'список продуктов <b>через пробел</b>, чтобы добавить.'
    sent = bot.send_message(message.chat.id, reccomendation_text, parse_mode='HTML')
    bot.register_next_step_handler(sent, update_shoplist)


# Telegram.message object -> void
def update_shoplist(message):
    text = message.text
    text = text.lower()
    text = text.split(' ')
    for i in range(len(text)):
        text[i] = text[i][0].upper() + text[i][1:]

    result_list = ShoppingList.get() + text
    result_list = set(result_list)
    result_list = list(result_list)

    ShoppingList.update(result_list)


# Weather and censorship section
# String -> void
def get_weather(chatid):
    weather, picture_name = Weather.get()
    print(picture_name)
    bot.send_message(chatid, weather)
    with open(picture_name, 'rb') as weather_icon:
        print(os.getcwd())
        print(os.listdir)
        bot.send_photo(chatid, weather_icon)

# string -> boolean
def contains_bad_words(text):
    return text in ['плохой', 'какашка', 'шындырск']


@bot.message_handler(commands=['start'])
def starting_menu(message):
    # starting_message - variable in config for starting message
    bot.send_message(message.chat.id, starting_message)
    bot.delete_message(message.chat.id, message.id)


@bot.message_handler(content_types=['text'])
def main(message):
    message_handler(message)


if __name__ == '__main__':
    while True:
        try:
            print('Включение', str(datetime.datetime.now().time())[:8])
            bot.polling(none_stop=True)
        finally:
            print('Выключение' + str(datetime.time())[:8])

