"""
Этот модуль отвечает за отслеживание событий
если пользователь что-то написал то команды для дальнейших действий
будет отдавать именно этот файл
"""
import telebot
import configparser
from telebot import types  # для указание типов

from src.telegram.processor.processor import Processor


class Events:
    def __init__(self, bot):
        self.bot = bot
        self.processor = Processor(bot)

    def start_listener(self):
        tg_bot = self.bot

        config = configparser.ConfigParser()
        config.read("src/resourses/properties.ini")

        @tg_bot.message_handler(commands=["start"])
        def say_hello(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(config.get("BUTTON", "eng_test_text") + "📖")
            btn2 = types.KeyboardButton(config.get("BUTTON", "get_contact") + "😎🤘")
            btn3 = types.KeyboardButton(config.get("BUTTON", "get_anik") + "😂")
            markup.add(btn1, btn2, btn3)
            tg_bot.send_message(message.chat.id,
                                text="Привет,{0.first_name}!\n".format(
                                    message.from_user) + config.get("DEFAULT", "start_message") + "🤓",
                                reply_markup=markup)

        @tg_bot.message_handler(content_types=['text'])
        def button_responser(message):
            if message.text == (config.get("BUTTON", "eng_test_text") + "📖"):
                self.processor.assess_eng_level(message)
            elif message.text == (config.get("BUTTON", "get_contact") + "😎🤘"):
                self.processor.send_contact(message)
            elif message.text == (config.get("BUTTON", "get_anik") + "😂"):
                self.processor.send_anik(message)

        tg_bot.polling()
