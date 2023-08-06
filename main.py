import configparser
import logging

import telebot

from src.storage.storage import Storage
from src.telegram.events.events import Events
from src.telegram.processor.processor import Processor

config = configparser.ConfigParser()
config.read("src/resourses/api_key.ini")
TOKEN = config.get("KEY", "api_key")  # api бота, которое хранится в файле api_key.ini


def main():
    logging.basicConfig(level=logging.ERROR, filename="logs.log", filemode="w", encoding='utf-8')
    loger = logging.getLogger("loger")
    storage = Storage(loger)
    storage.open_connect()
    bot = telebot.TeleBot(TOKEN)  # Создаю экземпляр бота
    processor = Processor(bot, storage, loger)
    events = Events(bot, processor, loger)  # Создаю экземпляр events-ов для взаимодействия с api-телеграма
    events.start_listener()  # Запускаю "слушатель", который ходит на сервер и проверяет наличие ивентов


if __name__ == '__main__':
    main()
