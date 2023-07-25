import configparser
import threading

from src.storage.eng.eng import Eng_storage


class Preparation_before_save_bd:
    test_is_over = False
    user = None

    def __init__(self, test, message):
        self.test = test
        self.message = message
        self.eng_storage = Eng_storage(self.test.storage.connect)
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

    # Если тест не был завершён до таймера, то завершает его в этом методе
    def result_processing_if_test_is_over(self):
        if self.test_is_over is True:
            return
        if (len(self.test.answers) + 1) == int(self.test.test_config.get("DEFAULT", "questions_score")):
            return
        self.test.result_processing(self.message)

    # Сохраняет юзера, если тест не был завершён
    def save_new_user(self):
        if self.test_is_over is True:
            return
        self.eng_storage.save_new_user(self.user)

    # Запускает метод и закрывает его по истечению таймера
    def run_after_delay(self, delay, func, *args):
        timer = threading.Timer(delay, func, args=args)
        timer.start()

    # Собирает в словать пользователя
    def collect_result_for_db(self):
        user = {
            'id': self.message.from_user.id,
            'username': self.message.from_user.username,
            'test_result': self.test.incorrect_answers,
            'correct_answer': self.test.correct_answer
        }
        return user

    # Вызывает метод из бд со всеми преподователями
    def get_all_teacher(self):
        if self.test_is_over is True:
            return
        teachers = self.eng_storage.get_teachers_id()
        self.teachers = teachers

    # Отправляет преподам сообщение о завершении теста
    def send_message_teachers(self):
        if self.test_is_over is True:
            return
        incorrect_answer = ""

        for i in self.user["test_result"]:
            incorrect_answer += "\n" + i + "\n"

        for teacher in self.teachers:
            chat = self.test.bot.get_chat(teacher[2])
            self.test.bot.send_message(chat.id,
                                       "Привет ," + teacher[1] +
                                       self.test.test_config.get("MESSAGE_TO_TEACHER", "user") + str(
                                           self.user["username"]) + " " +
                                       self.test.test_config.get("MESSAGE_TO_TEACHER",
                                                                 "complete_test") + incorrect_answer
                                       )
