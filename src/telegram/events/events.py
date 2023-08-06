"""
Этот модуль отвечает за отслеживание событий
если пользователь что-то написал то команды для дальнейших действий
будет отдавать именно этот файл
"""

import configparser
import threading

from src.errors.errors import Failed_start_test_passing_with_new_thread, Failed_send_anik, Failed_send_contact, \
    Failed_create_main_menu_buttons, Failed_start_message
from src.telegram.processor.assess_eng_level.operations_after_test import Operations_after_test
from src.telegram.processor.assess_eng_level.testing import Test


class Events:
    errors_config = configparser.ConfigParser()
    errors_config.read("src/resourses/errors_text.ini")

    # todo прописать /menu
    def __init__(self, bot, processor, loger):
        self.loger = loger
        self.bot = bot
        self.processor = processor
        self.eng_test = Test(self.bot, self.processor.storage, self.loger)

    def start_listener(self):

        operations_after_test = Operations_after_test(self.bot, self.processor, self.loger)

        # Когда просиходит /start, он вызывает методы, которые создают кнопки для меню и приветствуют юзера
        @self.bot.message_handler(commands=["start"])
        def salutatory(message):
            try:
                self.processor.storage.save_new_user(
                    {"username": "@" + message.from_user.username, "chat_id": message.chat.id})
                markup = self.processor.create_start_button()
                hello_text = "Привет,{0.first_name}".format(
                    message.from_user) + "😘\n" + self.processor.config.get("DEFAULT", "start_message")
                self.processor.send_start_message(message, markup, hello_text)
                explanatory_text = self.processor.config.get("DEFAULT", "explanatory_text") + "❤️"
                self.processor.send_start_message(message, markup, explanatory_text)
                self.bot.send_sticker(message.chat.id,
                                      "CAACAgIAAxkBAAKjJmTJHkvBdjbWSGbQ_vrCrkFzhAmRAAIFAAPANk8T-WpfmoJrTXUvBA")
            except Failed_start_message as e:
                print(self.errors_config.get("Events_errors", "failed_start_command") + str(e))

        # Метод отслеживает сообщения о входе в главное меню и если оно есть, то вызывает кнопки главного меню
        @self.bot.message_handler(
            func=lambda message: message.text == (self.processor.config.get("DEFAULT", "main_menu") + "➡️"))
        def take_main_menu(message):
            try:
                markup = self.processor.create_start_button()
                self.bot.send_message(message.chat.id, self.processor.config.get("DEFAULT", "main_menu") + "➡️",
                                      reply_markup=markup)
            except Failed_create_main_menu_buttons as e:
                print(self.errors_config.get("Events_errors", "failed_take_main_menu") + str(e))

        # Ждёт запроса на контакты от пользователя и вызывает метод, который их отправит
        @self.bot.message_handler(
            func=lambda message: message.text == (self.processor.config.get("BUTTON", "get_contact") + "😎🤘"))
        def contact_button_listener(message):
            try:
                self.processor.send_contact(message)
            except Failed_send_contact as e:
                print(self.errors_config.get("Events_errors", "failed_send_contact") + str(e))

        # Открывает меню с кнопками по английскому
        @self.bot.message_handler(
            func=lambda message: message.text == (self.processor.config.get("BUTTON", "eng") + "🇬🇧"))
        def open_eng_menu(message):
            try:
                markup = self.processor.create_eng_menu_button()
                self.bot.send_message(message.chat.id, self.processor.config.get("BUTTON", "eng") + "🇬🇧",
                                      reply_markup=markup)
            except Failed_start_test_passing_with_new_thread as e:
                print(self.errors_config.get("Events_errors", "failed_test_start") + str(e))

        # Открывает меню с кнопками по программированию
        @self.bot.message_handler(
            func=lambda message: message.text == (self.processor.config.get("BUTTON", "programming") + "🖥"))
        def open_programming_menu(message):
            try:
                markup = self.processor.create_prog_menu_button()
                self.bot.send_message(message.chat.id, self.processor.config.get("BUTTON", "programming") + "🖥",
                                      reply_markup=markup)
            except Failed_start_test_passing_with_new_thread as e:
                print(self.errors_config.get("Events_errors", "failed_test_start") + str(e))

        @self.bot.message_handler(
            func=lambda message: message.text == (self.processor.config.get("BUTTON", "eng_test_text") + "📖"))
        def assess_eng_level_button_listener(message):
            try:
                if not self.processor.storage.get_current_test_object_by_chat_id(message.chat.id):
                    self.processor.storage.add_current_test_object(message.chat.id, "English")
                else:
                    self.processor.storage.set_current_test_object_by_chat_id(message.chat.id, "English")

                if not self.processor.eng_storage.get_user_by_chat_id(message.chat.id):
                    self.processor.eng_storage.save_new_eng_user({
                        "username": "@" + message.from_user.username,
                        "chat_id": message.chat.id,
                        "test_status": "inProcess",
                        "current_question": "1",
                        "mistakes": "",
                        "correct_answer": 0,
                    })
                user = self.processor.eng_storage.get_user_by_chat_id(message.chat.id)
                if user[0][3] == "inProcess":
                    markup = self.eng_test.create_answer_button()
                    self.eng_test.send_question(message, user[0][4], markup)
                if user[0][3] == "isOver":
                    markup = self.eng_test.create_eng_menu_button()
                    self.eng_test.send_notification_test_already_completion(message, markup)
            except Failed_start_test_passing_with_new_thread as e:
                print(self.errors_config.get("Events_errors", "failed_test_start") + str(e))

        # Ждёт запроса на аник от пользователя и отправляет его, если запрос есть
        @self.bot.message_handler(
            func=lambda message: message.text == (self.processor.config.get("BUTTON", "get_anik") + "🥵🥵🥵"))
        def anik_button_listener(message):
            try:
                self.processor.send_anik(message)
            except Failed_send_anik as e:
                print(self.errors_config.get("Events_errors", "failed_send_anik") + str(e))

        @self.bot.message_handler(
            func=lambda message: message.text == self.processor.config.get("BUTTON", "show_teacher") + "👨‍🏫")
        def show_teachers_eng(message):
            try:
                markup = self.processor.create_eng_menu_button()
                self.processor.send_teacher_info(message, markup)
            except Exception as e:
                print(e)

        @self.bot.message_handler(
            func=lambda message: (message.text == "1") | (message.text == "2") | (message.text == "3") | (
                    message.text == "4"))
        def answer_the_question(message):
            try:
                current_test = self.processor.storage.get_current_test_object_by_chat_id(message.chat.id)[0][2]

                if current_test == "English":
                    user = self.processor.eng_storage.get_user_by_chat_id(message.chat.id)

                    if user[0][3] == "isOver":
                        markup = self.processor.create_eng_menu_button()
                        self.eng_test.send_notification_test_already_completion(message, markup)
                        return
                    current_question = self.eng_test.checking_answer(message, message.text)

                    if (int(current_question)) == (
                            int(self.eng_test.test_config.get("DEFAULT", "questions_score")) - 1):
                        self.processor.eng_storage.set_test_state_is_over(message.chat.id, "isOver")
                        correct_answers = int(self.eng_test.eng_storage.get_correct_answer(message.chat.id)[0][0])
                        level = self.eng_test.result_processing(correct_answers)
                        self.eng_test.send_notification_test_completion(message.chat.id, correct_answers, level)
                        teachers = self.eng_test.eng_storage.get_teachers_id()
                        self.eng_test.send_message_teachers(message.chat.id, teachers, message.from_user.username)
                        return

                    self.processor.eng_storage.set_next_question(message.chat.id, int(current_question))

                    markup = self.eng_test.create_answer_button()
                    self.eng_test.send_question(message, str(int(current_question) + 1), markup)

                if current_test == "Chemistry":
                    pass
            except Exception as e:
                print(e)

        @self.bot.message_handler(func=lambda message: True)
        def echo_all(message):
            self.bot.reply_to(message, message.text)

        self.bot.polling()  # Метод непрерывно проверяет наличие новых сообщений от юзера и перенаправляет их в методы выше
