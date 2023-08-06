"""
Тут будут запросы которые связаны чисто с английским
"""
import configparser

from src.errors.errors import Failed_save_user, Failed_get_teachers


class Eng_storage:
    def __init__(self, connect, loger):
        self.loger = loger
        self.connect = connect

    config = configparser.ConfigParser()
    config.read("src/resourses/errors_text.ini")

    # Сохраняет нового ученика по английскому
    def save_new_eng_user(self, user):
        try:
            with self.connect.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO eng_students (username,chat_id,test_status,current_question,mistakes,correct_answers) VALUES (%s,%s,"
                    "%s,%s,%s,%s)",
                    (user["username"],
                     user["chat_id"],
                     user["test_status"],
                     user["current_question"],
                     user["mistakes"],
                     user["correct_answer"]))
                self.connect.commit()
        except Failed_save_user as e:
            print(self.config.get("Database_errors", "failed_save_user") + str(e))

    # Устанавливает следующий вопрос
    def set_next_question(self, chat_id, current_question):
        try:
            with self.connect.cursor() as cursor:
                cursor.execute(
                    "UPDATE eng_students SET current_question = %s WHERE chat_id = %s;",
                    (str(current_question + 1), chat_id))
                self.connect.commit()
        except Failed_save_user as e:
            print(self.config.get("Database_errors", "failed_save_user") + str(e))

    # Ставит в бд состояние завершения теста
    def set_test_state_is_over(self, chat_id, test_status):
        try:
            with self.connect.cursor() as cursor:
                cursor.execute(
                    "UPDATE eng_students SET test_status = %s WHERE chat_id = %s;",
                    (test_status, chat_id))
                self.connect.commit()
        except Failed_save_user as e:
            print(self.config.get("Database_errors", "failed_save_user") + str(e))

    def get_user_mistake(self, chat_id):
        try:
            with self.connect.cursor() as cursor:
                cursor.execute(
                    "SELECT mistakes FROM eng_students WHERE chat_id = {0};".format(chat_id))
                mistakes = cursor.fetchall()
                return mistakes
        except Failed_save_user as e:
            print(self.config.get("Database_errors", "failed_save_user") + str(e))

    def add_test_mistake_to_user(self, chat_id, mistake):
        try:
            with self.connect.cursor() as cursor:
                cursor.execute(
                    "UPDATE eng_students SET mistakes = %s WHERE chat_id = %s;",
                    (mistake, chat_id))
                self.connect.commit()
        except Failed_save_user as e:
            print(self.config.get("Database_errors", "failed_save_user") + str(e))

    def add_correct_answer(self, chat_id):
        try:
            with self.connect.cursor() as cursor:
                cursor.execute(
                    "UPDATE eng_students SET correct_answers = correct_answers + 1 WHERE chat_id={0}".format(chat_id))
                self.connect.commit()
        except Failed_save_user as e:
            print(self.config.get("Database_errors", "failed_save_user") + str(e))

    def get_correct_answer(self, chat_id):
        try:
            with self.connect.cursor() as cursor:
                cursor.execute(
                    "SELECT correct_answers FROM eng_students WHERE chat_id={0}".format(chat_id))
                correct_answer = cursor.fetchall()
                return correct_answer
        except Failed_get_teachers as e:
            print(self.config.get("Database_errors", "failed_get_teachers_id") + str(e))

    # Получет всех преподователей
    def get_teachers_id(self):
        try:
            with self.connect.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM teachers")
                teachers = cursor.fetchall()
                return teachers
        except Failed_get_teachers as e:
            print(self.config.get("Database_errors", "failed_get_teachers_id") + str(e))

    # Возвращает пользователя по параметру "chat_id"
    def get_user_by_chat_id(self, chat_id):
        try:
            with self.connect.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM eng_students WHERE chat_id = {0}".format(chat_id))
                user = cursor.fetchall()
                return user
        except Failed_get_teachers as e:
            print(self.config.get("Database_errors", "failed_get_teachers_id") + str(e))

    def get_max_teacher_id(self):
        try:
            with self.connect.cursor() as cursor:
                cursor.execute(
                    "SELECT MAX(id) FROM teachers;")
                teacher = cursor.fetchall()
                return teacher
        except Failed_get_teachers as e:
            print(self.config.get("Database_errors", "failed_get_teachers_id") + str(e))
