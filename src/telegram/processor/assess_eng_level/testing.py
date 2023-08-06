import configparser
from telebot import types

from src.errors.errors import Failed_send_offer_take_test, Failed_send_question_eng_test, Failed_process_test_result, \
    Failed_send_test_result_to_user, Failed_create_test_button, Failed_create_main_menu_buttons, Failed_execution_test, \
    Failed_get_teachers, Failed_send_message_to_teacher
from src.logic.eng.estimation.estimation import Test_estimation
from src.storage.eng.eng_storage import Eng_storage
from src.telegram.processor.processor import Processor

"""
    Класс отвечает за проведение теста пользователя.
    Он умеет задавать вопросы, запоминать ответы на эти вопросы
    И умеет выводить результат
"""


class Test(Processor):
    def __init__(self, bot, storage, loger):
        self.bot = bot
        super().__init__(self.bot, storage, loger)

    config = configparser.ConfigParser()
    config.read("src/resourses/properties.ini")

    test_config = configparser.ConfigParser()
    test_config.read("src/resourses/test.ini")

    errors_config = configparser.ConfigParser()
    errors_config.read("src/resourses/errors_text.ini")

    # Отправка сообщения о том, что тест начинается
    def offer_take_test(self, message, markup):
        try:
            self.bot.send_message(message.chat.id, text=self.config.get("RESPONSE", "eng_test_response"),
                                  reply_markup=markup)
        except Failed_send_offer_take_test as e:
            print(self.errors_config.get("Assess_eng_lvl", "failed_send_offer_take_test") + str(e))

    # Отправляет вопрос пользователю
    def send_question(self, message, question, markup):
        try:
            self.bot.send_message(message.chat.id, self.test_config.get("QUESTION", "question_" + question),
                                  reply_markup=markup)
        except Exception as e:
            print(e)

    # Отправляет уведомление о том, что тест уже пройден
    def send_notification_test_already_completion(self, message, markup):
        self.bot.send_message(message.chat.id, self.test_config.get("DEFAULT", "test_already_is_over"),
                              reply_markup=markup)
        self.bot.send_message(message.chat.id, self.config.get("RESPONSE", "contact_response"), parse_mode="Markdown",
                              reply_markup=markup)

    def send_notification_test_completion(self, chat_id, correct_answer, level):
        try:
            if level == "low_level":
                self.bot.send_message(chat_id, text=self.test_config.get("RESULT", "test_result_before") + " " + str(
                    correct_answer) + " " + self.test_config.get("RESULT",
                                                                 "test_result_after") + self.test_config.get(
                    "RESULT", "lox"))
                self.bot.send_message(chat_id, self.config.get("RESPONSE", "contact_response"),
                                      parse_mode="Markdown")
            elif level == "medium_level":
                self.bot.send_message(chat_id, text=self.test_config.get("RESULT", "test_result_before") + " " + str(
                    correct_answer) + " " + self.test_config.get("RESULT",
                                                                 "test_result_after") + self.test_config.get(
                    "RESULT", "norm_lvl"))
                self.bot.send_message(chat_id, self.config.get("RESPONSE", "contact_response"),
                                      parse_mode="Markdown")
            elif level == "height_level":
                self.bot.send_message(chat_id, text=self.test_config.get("RESULT", "test_result_before") + " " + str(
                    correct_answer) + " " + self.test_config.get("RESULT",
                                                                 "test_result_after") + self.test_config.get(
                    "RESULT", "god"))
                self.bot.send_message(chat_id, self.config.get("RESPONSE", "contact_response"),
                                      parse_mode="Markdown")
        except Failed_send_test_result_to_user as e:
            print(self.errors_config.get("Assess_eng_lvl", "failed_send_test_result_to_user") + str(e))

    # Проверяет ответ пользователя
    def checking_answer(self, message, answer):
        user = self.eng_storage.get_user_by_chat_id(message.chat.id)
        if user:
            current_question = user[0][4]
            if answer == self.test_config.get("ANSWERS", "answer_" + str(current_question)):
                self.eng_storage.add_correct_answer(message.chat.id)
            else:
                mistake = self.eng_storage.get_user_mistake(message.chat.id)[0][0]
                mistake += "\n" + "\n" + "\n" + self.test_config.get("QUESTION", "question_" + str(current_question))
                self.eng_storage.add_test_mistake_to_user(message.chat.id, mistake)
            return current_question

    # Вызывает метод из бд со всеми преподователями
    def get_all_teacher(self):
        try:
            teachers = self.eng_storage.get_teachers_id()
        except Failed_get_teachers as e:
            print(self.errors_config.get("Database_errors", "failed_get_teachers_id") + str(e))

    # Определяет уроверь юзера
    def result_processing(self, correct_answer):
        if 3 > correct_answer >= 0:
            return "low_level"
        elif 5 > correct_answer >= 3:
            return "medium_level"
        elif correct_answer >= 5:
            return "height_level"

    # Отправляет преподам сообщение о завершении теста
    def send_message_teachers(self, chat_id, teachers, username):
        try:

            incorrect_answer = self.eng_storage.get_user_mistake(chat_id)[0][0]
            print(incorrect_answer)

            for teacher in teachers:
                chat = self.bot.get_chat(teacher[2])
                if incorrect_answer == "":
                    self.bot.send_message(chat.id,
                                          "Привет ," + teacher[1] +
                                          self.test_config.get("MESSAGE_TO_TEACHER", "user") + username + " " +
                                          self.test_config.get("MESSAGE_TO_TEACHER",
                                                               "complete_test_null_errors")
                                          )
                else:
                    self.bot.send_message(chat.id,
                                          "Привет ," + teacher[1] +
                                          self.test_config.get("MESSAGE_TO_TEACHER", "user") + username + " " +
                                          self.test_config.get("MESSAGE_TO_TEACHER",
                                                               "complete_test") + incorrect_answer
                                          )
        except Failed_send_message_to_teacher as e:
            print(self.errors_config.get("Assess_eng_lvl", "failed_send_message_to_teacher") + str(e))

    # Создаёт кнопки ответа на тест
    def create_answer_button(self):
        try:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("1")
            btn2 = types.KeyboardButton("2")
            btn3 = types.KeyboardButton("3")
            btn4 = types.KeyboardButton("4")
            btn5 = types.KeyboardButton(self.config.get("DEFAULT", "main_menu") + "➡️")
            markup.add(btn1, btn2, btn3, btn4, btn5)
            return markup
        except Failed_create_test_button as e:
            print(self.errors_config.get("Assess_eng_lvl", "failed_create_test_button") + str(e))

    # Функция которая создаёт кнопки главног меню
    def take_main_menu(self, message):
        try:
            markup = self.create_start_button()
            self.bot.send_message(message.chat.id, self.config.get("DEFAULT", "main_menu") + "➡️", reply_markup=markup)
        except Failed_create_main_menu_buttons as e:
            print(self.errors_config.get("Events_errors", "failed_take_main_menu") + str(e))
