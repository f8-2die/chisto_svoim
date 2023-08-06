import configparser
import threading
from datetime import datetime

from src.errors.errors import Failed_save_user, Failed_get_teachers, Failed_send_message_to_teacher, \
    Failed_run_after_delay_in_new_threading, Failed_get_user
from src.storage.eng.eng_storage import Eng_storage


class Preparation_before_save_bd:
    test_is_over = False
    user = None
    user_exist = False
    errors_config = configparser.ConfigParser()
    errors_config.read("src/resourses/errors_text.ini")

    def __init__(self, test, message, loger):
        self.loger = loger
        self.test = test
        self.message = message
        self.eng_storage = Eng_storage(self.test.storage.connect, self.loger)
        self.teachers = None

    # Проверяет закрыт ли экстренно тест
    def checking_test_completion(self):
        if self.test.end_test is True:
            self.test_is_over = True

    # Получает юзера, если тест не был закрыт
    def get_user(self):
        if self.test_is_over is True:
            return
        user = self.collect_result_for_db()
        self.user = user

    # Сохраняет юзера, если тест не был завершён
    def save_new_user(self):
        try:
            if (self.test_is_over is True) | (self.user_exist is True):
                return
            print(self.user)
            self.eng_storage.save_new_eng_user(self.user)
        except Failed_save_user as e:
            print(self.errors_config.get("Database_errors", "failed_save_user") + str(e))

    # Запускает метод и закрывает его по истечению таймера
    def run_after_delay(self, delay, func, *args):
        try:
            timer = threading.Timer(delay, func, args=args)
            timer.start()
        except Failed_run_after_delay_in_new_threading as e:
            print(self.errors_config.get("default", "failed_run_after_delay_in_new_threading") + str(e))

    # Собирает в словать пользователя
    def collect_result_for_db(self):
        user = {
            'id': self.message.from_user.id,
            'username': self.message.from_user.username,
            'test_result': self.test.incorrect_answers,
            'correct_answer': self.test.correct_answer,
        }
        return user

    # Вызывает метод из бд со всеми преподователями
    def get_all_teacher(self):
        try:
            if (self.test_is_over is True) | (self.user_exist is True):
                return
            teachers = self.eng_storage.get_teachers_id()
            self.teachers = teachers
        except Failed_get_teachers as e:
            print(self.errors_config.get("Database_errors", "failed_get_teachers_id") + str(e))

    # Отправляет преподам сообщение о завершении теста
    def send_message_teachers(self):
        try:
            if (self.test_is_over is True) | (self.user_exist is True):
                return
            incorrect_answer = ""

            for i in self.user["test_result"]:
                incorrect_answer += "\n" + i + "\n"
            for teacher in self.teachers:
                chat = self.test.bot.get_chat(teacher[2])
                if int(self.user["correct_answer"]) == int(self.test.test_config.get("DEFAULT", "questions_score")) + 1:
                    self.test.bot.send_message(chat.id,
                                               "Привет ," + teacher[1] +
                                               self.test.test_config.get("MESSAGE_TO_TEACHER", "user") + str(
                                                   self.user["username"]) + " " +
                                               self.test.test_config.get("MESSAGE_TO_TEACHER",
                                                                         "complete_test_null_errors")
                                               )
                else:
                    self.test.bot.send_message(chat.id,
                                               "Привет ," + teacher[1] +
                                               self.test.test_config.get("MESSAGE_TO_TEACHER", "user") + str(
                                                   self.user["username"]) + " " +
                                               self.test.test_config.get("MESSAGE_TO_TEACHER",
                                                                         "complete_test") + incorrect_answer
                                               )
        except Failed_send_message_to_teacher as e:
            print(self.errors_config.get("Assess_eng_lvl", "failed_send_message_to_teacher") + str(e))

    # Вызывает метод из бд, который даёт юзера, а потом, если он существует, меняет @user_exist на True
    def checking_existence_user(self):
        try:
            if self.user:
                user_in_db = self.eng_storage.get_user_by_chat_id(self.user["id"])
            else:
                return

            if user_in_db:
                print("Пользователь существует!")
                self.user_exist = True
            else:
                return
        except Exception as e:
            raise Failed_get_user(str(e))
