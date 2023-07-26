"""
Этот модуль будет исполнять команды отдаваемые events
"""
import configparser
from random import randint

from telebot import types  # для указание типов


class Processor:
    # создание экзепляра конфига
    config = configparser.ConfigParser()
    config.read("src/resourses/properties.ini")

    def __init__(self, bot, storage):
        self.bot = bot
        self.storage = storage

    # Пишет пользователю приветственное сообщение
    def say_hello(self, message, markup):
        self.bot.send_message(message.chat.id,
                              text="Привет,{0.first_name}!\n".format(
                                  message.from_user) + self.config.get("DEFAULT", "start_message") + "🤓",
                              reply_markup=markup)

    # Метод создаёт кнопки меню
    def create_start_button(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(self.config.get("BUTTON", "eng_test_text") + "📖")
        btn2 = types.KeyboardButton(self.config.get("BUTTON", "get_contact") + "😎🤘")
        btn3 = types.KeyboardButton(self.config.get("BUTTON", "get_anik") + "🥵🥵🥵")
        markup.add(btn1, btn2, btn3)
        return markup

    # Отправляет контакты на менеджера
    def send_contact(self, message):
        self.bot.send_message(message.chat.id, text=self.config.get("RESPONSE", "contact_response"))

    # Отправляет аник
    def send_anik(self, message):
        anik_config = configparser.ConfigParser()
        anik_config.read("src/resourses/aniki.ini")
        anik_number = randint(1, int(anik_config.get("DEFAULT", "anil_count")))
        self.bot.send_message(message.chat.id,
                              text=anik_config.get("ANIKI", "anik_" + str(anik_number)))
