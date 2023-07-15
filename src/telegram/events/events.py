"""
Этот модуль отвечает за отслеживание событий
если пользователь что-то написал то команды для дальнейших действий
будет отдавать именно этот файл
"""
import configparser

from src.telegram.processor.processor import Processor


class Events:
    def __init__(self, bot):
        self.bot = bot
        self.processor = Processor(bot)

    def start_listener(self):
        tg_bot = self.bot

        config = configparser.ConfigParser()
        config.read("src/resourses/properties.ini")

        # Когда просиходит /start, он вызывает методы, которые создают кнопки для меню и приветствуют юзера
        @tg_bot.message_handler(commands=["start"])
        def salutatory(message):
            markup = self.processor.create_start_button()
            self.processor.say_hello(message, markup)

        # Метод отслеживает сообщения о входе в главное меню и если оно есть, то вызывает кнопки главного меню
        @tg_bot.message_handler(
            func=lambda message: message.text == (config.get("DEFAULT", "main_menu") + "➡️"))
        def take_main_menu(message):
            markup = self.processor.create_start_button()
            self.bot.send_message(message.chat.id, config.get("DEFAULT", "main_menu") + "➡️", reply_markup=markup)

        # Ждёт запроса на контакты от пользователя и вызывает метод, который их отправит
        @tg_bot.message_handler(
            func=lambda message: message.text == (config.get("BUTTON", "get_contact") + "😎🤘"))
        def contact_button_listener(message):
            self.processor.send_contact(message)

        # Ждёт запроса на тест от пользователя и вызывает метод, который его запустит
        @tg_bot.message_handler(
            func=lambda message: message.text == (config.get("BUTTON", "eng_test_text") + "📖"))
        def assess_eng_level_button_listener(message):
            self.processor.assess_eng_level(message)

        # Ждёт запроса на аник от пользователя и отправляет его, если запрос есть
        @tg_bot.message_handler(
            func=lambda message: message.text == (config.get("BUTTON", "get_anik") + "😂"))
        def anik_button_listener(message):
            self.processor.send_anik(message)

        tg_bot.polling()  # Метод непрерывно проверяет наличие новых сообщений от юзера и перенаправляет их в методы выше
