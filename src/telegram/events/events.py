"""
Этот модуль отвечает за отслеживание событий
если пользователь что-то написал то команды для дальнейших действий
будет отдавать именно этот файл
"""

import configparser
import threading

from src.logic.eng.estimation.preporation_befor_save_bd import Preparation_before_save_bd
from src.telegram.processor.assess_eng_level.testing import Test


class Events:
    def __init__(self, bot, processor):
        self.bot = bot
        self.processor = processor

    '''
    Метод с задержкой в 2 минуты вызывает следующие методы: 
    1) Проверку завершён ли тест экстренно или же нормально
    2) Если нормально, то запускает обработку результатов и подготовку их для записи в БД
    3) Записывает в БД
    4) Пишет преподам, что тест был пройден
    '''

    def processing_save_user(self, message):
        test = Test(self.bot, self.processor.storage)  # создаёт экземпляр теста
        test.assess_eng_level(message)  # запускает метод с началом теста
        preparation_before_save_bd = Preparation_before_save_bd(test,
                                                                message)  # экземпляр класса с обработкой результатов
        preparation_before_save_bd.run_after_delay(125,
                                                   preparation_before_save_bd.checking_test_completion)  # проверяет закончен ли тест
        preparation_before_save_bd.run_after_delay(130,
                                                   preparation_before_save_bd.result_processing_if_test_is_over)  # обрабатывает результаты, если они не были обработаны
        preparation_before_save_bd.run_after_delay(133, preparation_before_save_bd.get_user)  # получает юзера
        preparation_before_save_bd.run_after_delay(135,
                                                   preparation_before_save_bd.save_new_user)  # сохраняет юзера в бд
        preparation_before_save_bd.run_after_delay(137,
                                                   preparation_before_save_bd.get_all_teacher)  # получает список преподов
        preparation_before_save_bd.run_after_delay(140,
                                                   preparation_before_save_bd.send_message_teachers)  # отправляет преподам сообщение о завершении теста юзером

    def start_listener(self):
        config = configparser.ConfigParser()
        config.read("src/resourses/properties.ini")

        # Когда просиходит /start, он вызывает методы, которые создают кнопки для меню и приветствуют юзера
        @self.bot.message_handler(commands=["start"])
        def salutatory(message):
            markup = self.processor.create_start_button()
            self.processor.say_hello(message, markup)

        # Метод отслеживает сообщения о входе в главное меню и если оно есть, то вызывает кнопки главного меню
        @self.bot.message_handler(
            func=lambda message: message.text == (config.get("DEFAULT", "main_menu") + "➡️"))
        def take_main_menu(message):
            markup = self.processor.create_start_button()
            self.bot.send_message(message.chat.id, config.get("DEFAULT", "main_menu") + "➡️", reply_markup=markup)

        # Ждёт запроса на контакты от пользователя и вызывает метод, который их отправит
        @self.bot.message_handler(
            func=lambda message: message.text == (config.get("BUTTON", "get_contact") + "😎🤘"))
        def contact_button_listener(message):
            self.processor.send_contact(message)

        # Запускает в новом потоке метод(processing_save_user), который запускает тест
        @self.bot.message_handler(
            func=lambda message: message.text == (config.get("BUTTON", "eng_test_text") + "📖"))
        def assess_eng_level_button_listener(message):
            thread = threading.Thread(target=self.processing_save_user(message))
            thread.start()
            thread.join(timeout=150)
            if thread.is_alive():
                thread.join()

        # Ждёт запроса на аник от пользователя и отправляет его, если запрос есть
        @self.bot.message_handler(
            func=lambda message: message.text == (config.get("BUTTON", "get_anik") + "😂"))
        def anik_button_listener(message):
            self.processor.send_anik(message)

        self.bot.polling()  # Метод непрерывно проверяет наличие новых сообщений от юзера и перенаправляет их в методы выше
