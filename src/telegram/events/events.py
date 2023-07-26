"""
Этот модуль отвечает за отслеживание событий
если пользователь что-то написал то команды для дальнейших действий
будет отдавать именно этот файл
"""

import configparser
import threading

from src.errors.errors import Failed_start_test_passing_with_new_thread, Failed_send_anik, Failed_send_contact, \
    Failed_create_main_menu_buttons, Failed_start_message, Failed_execution_test
from src.logic.eng.estimation.preporation_befor_save_bd import Preparation_before_save_bd
from src.telegram.processor.assess_eng_level.testing import Test


class Events:
    errors_config = configparser.ConfigParser()
    errors_config.read("src/resourses/errors_text.ini")

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
        try:
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
        except Failed_execution_test as e:
            print(self.errors_config.get("Events_errors", "failed_execute_test") + str(e))

    def start_listener(self):
        config = configparser.ConfigParser()
        config.read("src/resourses/properties.ini")

        # Когда просиходит /start, он вызывает методы, которые создают кнопки для меню и приветствуют юзера
        @self.bot.message_handler(commands=["start"])
        def salutatory(message):
            try:
                markup = self.processor.create_start_button()
                self.processor.say_hello(message, markup)
            except Failed_start_message as e:
                print(self.errors_config.get("Events_errors", "failed_start_command") + str(e))

        # Метод отслеживает сообщения о входе в главное меню и если оно есть, то вызывает кнопки главного меню
        @self.bot.message_handler(
            func=lambda message: message.text == (config.get("DEFAULT", "main_menu") + "➡️"))
        def take_main_menu(message):
            try:
                markup = self.processor.create_start_button()
                self.bot.send_message(message.chat.id, config.get("DEFAULT", "main_menu") + "➡️", reply_markup=markup)
            except Failed_create_main_menu_buttons as e:
                print(self.errors_config.get("Events_errors", "failed_take_main_menu") + str(e))

        # Ждёт запроса на контакты от пользователя и вызывает метод, который их отправит
        @self.bot.message_handler(
            func=lambda message: message.text == (config.get("BUTTON", "get_contact") + "😎🤘"))
        def contact_button_listener(message):
            try:
                self.processor.send_contact(message)
            except Failed_send_contact as e:
                print(self.errors_config.get("Events_errors", "failed_send_contact") + str(e))

        # Запускает в новом потоке метод(processing_save_user), который запускает тест
        @self.bot.message_handler(
            func=lambda message: message.text == (config.get("BUTTON", "eng_test_text") + "📖"))
        def assess_eng_level_button_listener(message):
            try:
                thread = threading.Thread(target=self.processing_save_user(message))
                thread.start()
                thread.join(timeout=150)
                if thread.is_alive():
                    thread.join()
            except Failed_start_test_passing_with_new_thread as e:
                print(self.errors_config.get("Events_errors", "failed_test_start") + str(e))

        # Ждёт запроса на аник от пользователя и отправляет его, если запрос есть
        @self.bot.message_handler(
            func=lambda message: message.text == (config.get("BUTTON", "get_anik") + "🥵🥵🥵"))
        def anik_button_listener(message):
            try:
                self.processor.send_anik(message)
            except Failed_send_anik as e:
                print(self.errors_config.get("Events_errors", "failed_send_anik") + str(e))

        self.bot.polling()  # Метод непрерывно проверяет наличие новых сообщений от юзера и перенаправляет их в методы выше
