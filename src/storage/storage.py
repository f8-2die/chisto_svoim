"""
Этот модуль запускает полную бд
"""
import psycopg2
import configparser

from src.errors.errors import Failed_connect_bd, Failed_save_user


class Storage:
    db_config = configparser.ConfigParser()
    db_config.read("src/resourses/storage_config.ini")
    errors_config = configparser.ConfigParser()
    errors_config.read("src/resourses/errors_text.ini")
    connect = None

    def __init__(self, loger):
        self.loger = loger

    def open_connect(self):
        try:
            self.connect = psycopg2.connect(
                host=self.db_config.get("DEFAULT", "host"),
                user=self.db_config.get("DEFAULT", "user"),
                password=self.db_config.get("DEFAULT", "password"),
                database=self.db_config.get("DEFAULT", "db_name")
            )
            return self.connect
        except Failed_connect_bd as e:
            print(self.errors_config.get("Database_errors", "failed_open_db_connect") + str(e))

    def save_new_user(self, user):
        try:
            with self.connect.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (username,chat_id) VALUES (%s,%s)", (user["username"],
                                                                            user["chat_id"]))
                self.connect.commit()
        except Failed_save_user as e:
            print(self.config.get("Database_errors", "failed_save_user") + str(e))

    # Получает предмет по которому юзер проходит тест в данный момент
    def get_current_test_object_by_chat_id(self, chat_id):
        try:
            with self.connect.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM current_test WHERE chat_id = {0}".format(chat_id))
                user = cursor.fetchall()
                return user
        except Failed_save_user as e:
            print(self.config.get("Database_errors", "failed_save_user") + str(e))

    # Устанавливает предмет по которому юзер проходит тест в данный момент
    def set_current_test_object_by_chat_id(self, chat_id, subject):
        try:
            with self.connect.cursor() as cursor:
                cursor.execute(
                    "UPDATE current_test SET subject = %s WHERE chat_id = %s;", (subject, chat_id))
                self.connect.commit()
        except Failed_save_user as e:
            print(self.config.get("Database_errors", "failed_save_user") + str(e))

    # Добавляет юзера в таблицу с текущим тестом и устанавливает предмет
    def add_current_test_object(self, chat_id, subject):
        try:
            with self.connect.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO current_test (chat_id,subject) VALUES (%s,%s)", (chat_id, subject))
                self.connect.commit()
        except Failed_save_user as e:
            print(self.config.get("Database_errors", "failed_save_user") + str(e))

    def close_connect(self):
        self.connect.close()
