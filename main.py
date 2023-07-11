import configparser

import telebot

from src.telegram.events.events import Events

config = configparser.ConfigParser()
config.read("src/resourses/api_key.ini")
TOKEN = config.get("KEY", "api_key")


# эта функция будет ТОЧНО создавать самого bot и передавать в его в events
def main():
    bot = telebot.TeleBot(TOKEN)  # Создаю экземпляр бота

    events = Events(bot)  # Создаю экземпляр events-ов для взаимодействия с api-телеграма
    events.start_listener()  # Запускаю "слушатель", который ходит на сервер и проверяет наличие ивентов


if __name__ == '__main__':
    main()
