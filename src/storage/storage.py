"""
Этот модуль запускает полную бд
"""
import psycopg2
import configparser

from src.errors.errors import Failed_connect_bd


class Storage:
    db_config = configparser.ConfigParser()
    db_config.read("src/resourses/storage_config.ini")
    errors_config = configparser.ConfigParser()
    errors_config.read("src/resourses/errors_text.ini")
    connect = None

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

    def close_connect(self):
        self.connect.close()
