"""
Этот модуль будет исполнять команды отдаваемые events
если events отследил что нужно что-то сохранить в бд
то он вызовет метод из этого модуля а этот метод уже будет вызывать бд и делать всё что нужно
"""
import configparser


class Processor:
    config = configparser.ConfigParser()
    config.read("src/resourses/properties.ini")

    def __init__(self, bot):
        self.bot = bot

        # Н
    def assess_eng_level(self, message):
        tg_bot = self.bot
        tg_bot.send_message(message.chat.id, text=self.config.get("RESPONSE", "eng_test_response"))

    def send_contact(self, message):
        tg_bot = self.bot
        tg_bot.send_message(message.chat.id, text=self.config.get("RESPONSE", "contact_response"))

    def send_anik(self, message):
        tg_bot = self.bot
        tg_bot.send_message(message.chat.id,
                            text=self.config.get("RESPONSE", "anik_response"))
