"""
Тут будут запросы которые связаны чисто с английским
"""
import configparser

from src.errors.errors import Failed_save_user, Failed_get_teachers


class Eng_storage:
    def __init__(self, connect):
        self.connect = connect

    config = configparser.ConfigParser()
    config.read("src/resourses/errors_text.ini")

    def save_new_user(self, user):
        try:
            with self.connect.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (username,correct_answer) VALUES (%s, %s)", (user["username"],
                                                                                    user["correct_answer"]))
                self.connect.commit()
        except Failed_save_user as e:
            print(self.config.get("Database_errors", "failed_save_user"))

    def get_teachers_id(self):
        try:
            with self.connect.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM teachers")
                teachers = cursor.fetchall()
                return teachers
        except Failed_get_teachers as e:
            print(self.config.get("Database_errors", "failed get teachers id"))
