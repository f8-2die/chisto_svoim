"""
Этот модуль будет исполнять команды отдаваемые events
"""
import configparser
from random import randint

from telebot import types  # для указание типов

from src.errors.errors import Failed_send_helloMessage_to_user, Failed_create_start_button, Failed_send_contact, \
    Failed_send_anik


class Processor:
    # создание экзепляра конфига
    config = configparser.ConfigParser()
    config.read("src/resourses/properties.ini")
    errors_config = configparser.ConfigParser()
    errors_config.read("src/resourses/errors_text.ini")

    def __init__(self, bot, storage):
        self.bot = bot
        self.storage = storage

    # Пишет пользователю приветственное сообщение
    def say_hello(self, message, markup):
        try:
            self.bot.send_message(message.chat.id,
                                  text="Привет,{0.first_name}!\n".format(
                                      message.from_user) + self.config.get("DEFAULT", "start_message") + "🤓",
                                  reply_markup=markup)
        except Failed_send_helloMessage_to_user as e:
            print(self.errors_config.get("Processor_errors", "failed_send_hello") + str(e))

    # Метод создаёт кнопки меню
    def create_start_button(self):
        try:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(self.config.get("BUTTON", "eng_test_text") + "📖")
            btn2 = types.KeyboardButton(self.config.get("BUTTON", "get_contact") + "😎🤘")
            btn3 = types.KeyboardButton(self.config.get("BUTTON", "get_anik") + "🥵🥵🥵")
            markup.add(btn1, btn2, btn3)
            return markup
        except Failed_create_start_button as e:
            print(self.errors_config.get("Processor_errors", "failed_create_start_button") + str(e))

    # Отправляет контакты на менеджера
    def send_contact(self, message):
        try:
            self.bot.send_message(message.chat.id, text=self.config.get("RESPONSE", "contact_response"))
        except Failed_send_contact as e:
            print(self.errors_config.get("Events_errors", "failed_send_contact") + str(e))

    # Отправляет аник
    def send_anik(self, message):
        try:
            anik_config = configparser.ConfigParser()
            anik_config.read("src/resourses/aniki.ini")
            anik_number = randint(1, int(anik_config.get("DEFAULT", "anil_count")))
            self.bot.send_message(message.chat.id,
                                  text=anik_config.get("ANIKI", "anik_" + str(anik_number)))
        except Failed_send_anik as e:
            print(self.errors_config.get("Events_errors", "failed_send_anik") + str(e))
