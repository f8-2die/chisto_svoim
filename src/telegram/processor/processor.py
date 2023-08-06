"""
Этот модуль будет исполнять команды отдаваемые events
"""
import configparser
import logging
from random import randint

from telebot import types  # для указание типов

from src.errors.errors import Failed_send_helloMessage_to_user, Failed_create_start_button, Failed_send_contact, \
    Failed_send_anik
from src.storage.eng.eng_storage import Eng_storage


class Processor:
    # создание экзепляра конфига
    config = configparser.ConfigParser()
    config.read("src/resourses/properties.ini")
    errors_config = configparser.ConfigParser()
    errors_config.read("src/resourses/errors_text.ini")

    def __init__(self, bot, storage, loger):
        self.loger = loger
        self.bot = bot
        self.storage = storage
        self.eng_storage = Eng_storage(self.storage.connect, self.loger)

    # Пишет пользователю приветственное сообщение
    def send_start_message(self, message, markup, text):
        try:
            self.bot.send_message(message.chat.id,
                                  text=text,
                                  reply_markup=markup, parse_mode="Markdown")
        except Failed_send_helloMessage_to_user as e:
            print(self.errors_config.get("Processor_errors", "failed_send_hello") + str(e))

    # Метод создаёт кнопки меню
    def create_start_button(self):
        try:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(self.config.get("BUTTON", "eng") + "🇬🇧")
            btn2 = types.KeyboardButton(self.config.get("BUTTON", "programming") + "🖥")
            btn3 = types.KeyboardButton(self.config.get("BUTTON", "get_contact") + "😎🤘")
            btn4 = types.KeyboardButton(self.config.get("BUTTON", "get_anik") + "🥵🥵🥵")
            markup.add(btn1, btn2, btn3, btn4)
            return markup
        except Failed_create_start_button as e:
            print(self.errors_config.get("Processor_errors", "failed_create_start_button") + str(e))

    # Метод показывает кнопки меню английского
    def create_eng_menu_button(self):
        try:
            markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
            btn1 = types.KeyboardButton(self.config.get("BUTTON", "eng_test_text") + "📖")
            btn2 = types.KeyboardButton(self.config.get("BUTTON", "show_teacher") + "👨‍🏫")
            btn3 = types.KeyboardButton(self.config.get("DEFAULT", "main_menu") + "➡️")
            markup.add(btn1, btn2, btn3)
            return markup
        except Exception as e:
            print(e)

    # Отправляет список преподователей по английскому юзеру
    def send_teacher_info(self, message, markup):
        try:
            teacher = self.eng_storage.get_max_teacher_id()
            max_teacher_id = int(teacher[0][0])
            for i in range(2, max_teacher_id + 1):
                self.bot.send_message(message.chat.id, self.config.get("TEACHERS_DESCRIPTION", str(i) + "_teacher"),
                                      parse_mode="Markdown")
                with open('src/resourses/teachers_photo/' + str(i) + '.jpg', 'rb') as photo:
                    self.bot.send_photo(message.chat.id, photo, reply_markup=markup)
        except Exception as e:
            print(e)

    # Метод показывает кнопки меню программирования
    def create_prog_menu_button(self):
        try:
            markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
            btn1 = types.KeyboardButton(self.config.get("BUTTON", "programming_wishes") + "⌨️")
            btn2 = types.KeyboardButton(self.config.get("BUTTON", "show_teacher") + "👨‍💻")
            btn3 = types.KeyboardButton(self.config.get("DEFAULT", "main_menu") + "➡️")
            markup.add(btn1, btn2, btn3)
            return markup
        except Exception as e:
            print(e)

    # Отправляет контакты на менеджера
    def send_contact(self, message):
        try:
            self.bot.send_message(message.chat.id, text=self.config.get("RESPONSE", "contact_response"),
                                  parse_mode="Markdown")
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
