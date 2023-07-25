import configparser

import telebot

from src.storage.storage import Storage
from src.telegram.events.events import Events
from src.telegram.processor.processor import Processor

config = configparser.ConfigParser()
config.read("src/resourses/api_key.ini")
TOKEN = config.get("KEY", "api_key")  # api бота, которое хранится в файле api_key.ini


def main():
    storage = Storage()
    storage.open_connect()
    bot = telebot.TeleBot(TOKEN)  # Создаю экземпляр бота
    processor = Processor(bot, storage)
    events = Events(bot, processor)  # Создаю экземпляр events-ов для взаимодействия с api-телеграма
    events.start_listener()  # Запускаю "слушатель", который ходит на сервер и проверяет наличие ивентов


if __name__ == '__main__':
    main()
