import datetime
import time

from telebot import TeleBot, types

from collections import OrderedDict

from BinApi import ShoppingList
from Weather_api import Weather
from config import token, starting_message

bot = TeleBot(token)


# This is a main tree of received message.
# Функция перераспределяет запросы пользователей по функциям.
# Telegram.message object -> void
def message_handler(message):
    #  ГЛАВНОЕ МЕНЮ
    command = message.text.lower().strip()
    functions_dict = {'список продуктов': show_shopping_menu,
                      'посмотреть список продуктов': get_shopping_list,
                      'добавить продукты': shoplist_update_handler
                      }
    commands_list = ['меню', '@renatakamilabot', 'старт', 'начать', 'привет', 'назад']
    if command in commands_list:
        # bot.send_message(message.chat.id,message.chat.id)
        # bot.send_message(message.chat.id, message.json['from']['first_name'])
        show_main_menu(message)

    #  WEATHER SECTION
    #  Послать погоду на сегодня
    elif command == 'погода':
        get_weather(message.chat.id)

    #  FOODSTUFF LIST SECTION
    #  Раздел списка продуктов
    elif command in functions_dict.keys():
        functions_dict[command](message)

    elif command == 'очистить':
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
    bot.send_message(message.chat.id, 'Вот список моих функций на сегодня. Пользуйся :) ',
                     reply_markup=menu)


# These funcs gives a user a FOODSTUFF section buttons
# Telegram.message object -> void
def show_shopping_menu(message):
    bot.delete_message(message.chat.id, message.id)
    btn_back = types.KeyboardButton(text='Назад')
    btn_show_shopping_list = types.KeyboardButton(text='Посмотреть список продуктов')
    btn_add_to_shopping_list = types.KeyboardButton(text='Добавить продукты')

    shopping_menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    shopping_menu.add(btn_back, btn_show_shopping_list, btn_add_to_shopping_list)
    bot.send_message(message.chat.id, 'Ты можешь посмотреть или добавить в список продуктов ',
                     reply_markup=shopping_menu)


# shopping list button
# Telegram.message object -> void
def get_shopping_list(message):
    bot.delete_message(message.chat.id, message.id)
    bot.send_message(message.chat.id, '<b>Текущий список покупок:</b>', parse_mode='HTML')
    bot.send_message(message.chat.id, ', '.join(ShoppingList.get()))


# Telegram.message object -> void
def shoplist_update_handler(message):
    recommendation_text = 'В следующем предложении ты можешь написать ' \
                          'список продуктов <b>через пробел</b>, чтобы добавить.'
    sent = bot.send_message(message.chat.id, recommendation_text, parse_mode='HTML')
    bot.register_next_step_handler(sent, update_shoplist)


# Telegram.message object -> void
def update_shoplist(message):
    text = message.text
    text = text.lower()
    text = text.split(' ')
    text = [string.capitalize() for string in text]
    result_list = ShoppingList.get() + text
    result_list = list(OrderedDict.fromkeys(result_list))
    # сохраняет порядок в списке

    ShoppingList.update(result_list)


# Weather and censorship section
# String -> void
def get_weather(chat_id):
    weather, picture_name = Weather.get()
    # print(picture_name)
    bot.send_message(chat_id, weather)
    with open(picture_name, 'rb') as weather_icon:
        # print(os.getcwd())
        # print(os.listdir)
        bot.send_photo(chat_id, weather_icon)


# string -> boolean
def contains_bad_words(text):
    return text.lower() in ['плохой', 'какашка', 'сыктывкар']


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
        except RuntimeError:
            time.sleep(15)
        finally:
            print('Выключение' + str(datetime.time())[:8])
