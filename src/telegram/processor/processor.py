"""
Этот модуль будет исполнять команды отдаваемые events
"""
import configparser
import time

from telebot import types  # для указание типов

from src.logic.eng.estimation.estimation import Test_estimation
from src.telegram.processor.assess_eng_level.testing import Test


class Processor:
    # создание экзепляра конфига
    config = configparser.ConfigParser()
    config.read("src/resourses/properties.ini")

    def __init__(self, bot):
        self.bot = bot

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
        btn3 = types.KeyboardButton(self.config.get("BUTTON", "get_anik") + "😂")
        markup.add(btn1, btn2, btn3)
        return markup

    """
    Метод создаёт два класса: Test и Test_estimation.
    Вызывает методы, которые сначала задают вопросы юзеру
    А затем оценивают результат теста
    Затем же озвучивают результат теста
    """

    # todo ещё этот метод должен вызывать сохранение в БД юзера, а новый метод должен сразу же брать нового юзера и слать манагеру
    # todo рандомный порядок ответов на вопросы
    # todo чтобы в каких местах были ответы присылалось учителю
    def assess_eng_level(self, message):
        test = Test(self.bot, Processor(self.bot))
        markup = test.create_answer_button()
        test.offer_take_test(message, markup)  # пишет юзеру что тест начался
        test.start_test()  # запускает тест
        test.send_question(message)  # задаёт первый вопрос

    # Отправляет контакты на менеджера
    def send_contact(self, message):
        self.bot.send_message(message.chat.id, text=self.config.get("RESPONSE", "contact_response"))

    # Отправляет аник
    def send_anik(self, message):
        self.bot.send_message(message.chat.id,
                              text=self.config.get("RESPONSE", "anik_response"))
