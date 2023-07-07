"""
Этот модуль отвечает за отслеживание событий
если пользователь что-то написал то команды для дальнейших действий
будет отдавать именно этот файл
"""
import telebot
import configparser


class Events:
    def __init__(self, bot):
        self.bot = bot

    def start_listener(self):
        tg_bot = self.bot

        config = configparser.ConfigParser()
        config.read("src/resourses/properties.ini")

        @tg_bot.message_handler(commands=["start"])
        def say_hello(message):
            tg_bot.send_message(message.chat.id, config.get("DEFAULT", "start_message"))

        tg_bot.polling()
