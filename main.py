import telebot

from src.telegram.events.events import Events

TOKEN = "6383973511:AAFMJBhyVwdV1PmNSfeT4zlycw3EsHNICTU"


# эта функция будет ТОЧНО создавать самого bot и передавать в его в events
def main():
    bot = telebot.TeleBot(TOKEN)  # Создаю экземпляр бота

    events = Events(bot)  # Создаю экземпляр events-ов для взаимодействия с api-телеграма
    events.start_listener()  # Запускаю "слушатель", который ходит на сервер и проверяет наличие ивентов


if __name__ == '__main__':
    main()
