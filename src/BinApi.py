import os
import pickle

from Famaly_chat_Telegram_bot.src.config import admin_chat_id


# This is a DAO Data Access Object to work with .db (binary file, where i store an array)
class ShoppingList:

    # No params -> list of string
    @staticmethod
    def get():
        with open("../data/shoplistfile.bin", 'rb') as file:
            list_of_strings = pickle.load(file)
            return list_of_strings

    # list of string -> void
    @staticmethod
    def update(new_list):
        with open("../data/shoplistfile.bin", 'wb') as file:
            pickle.dump(new_list, file)

    # int -> void
    @staticmethod
    def delete(chat_id):
        if chat_id == admin_chat_id:
            print('p')
            starting_list = ['Хлеб']
            with open("../data/shoplistfile.bin", 'wb') as file:
                pickle.dump(starting_list, file)

if __name__ =="__main__":

    starting_list = ['Хлеб', 'Айран']
    with open("../data/shoplistfile.bin", 'wb') as file:
        pickle.dump(starting_list, file)