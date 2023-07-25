"""
Этот модуль запускает полную бд
"""
import psycopg2
import configparser


class Storage:
    db_config = configparser.ConfigParser()
    db_config.read("src/resourses/storage_config.ini")
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
        except Exception as _ex:
            print(_ex)
            # todo доделать блок ошибок и для БД

    def close_connect(self):
        self.connect.close()
