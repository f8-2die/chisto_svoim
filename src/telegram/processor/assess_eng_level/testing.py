import configparser
from telebot import types

"""
    Класс отвечает за проведение теста пользователя.
    Он умеет задавать вопросы, запоминать ответы на эти вопросы
    И умеет выводить результат
"""


class Test:
    current_question = 0  # Номер текущего вопроса
    correct_answer = 0  # Количество правильных ответов
    answers = []  # Список с ответами пользователя

    def __init__(self, bot, processor):
        self.bot = bot
        self.processor = processor

    config = configparser.ConfigParser()
    config.read("src/resourses/properties.ini")

    test_config = configparser.ConfigParser()
    test_config.read("src/resourses/test.ini")

    # Отправка сообщения о том, что тест начинается
    def offer_take_test(self, message, markup):
        self.bot.send_message(message.chat.id, text=self.config.get("RESPONSE", "eng_test_response"),
                              reply_markup=markup)

    # Старт теста
    def start_test(self, message):
        self.answers = []
        self.current_question = 0
        self.correct_answer = 0
        self.send_question(message)

    """
        Проверяет, есть ли запрос на выход из теста 
        Затем, если число отправленных вопросов меньше количества вопросов,то отправляет вопрос 
        Если число отправленных вопросов и общее их число равно, то вызывает функцию проверки результата и функцию 
        оповещения о результате пользователя.
    """

    def send_question(self, message):
        if message.text == self.config.get("DEFAULT", "main_menu") + "➡️":
            self.take_main_menu(message)
            return
        self.current_question += 1
        if self.current_question < int(self.test_config.get("DEFAULT", "questions_score")):
            msg = self.bot.send_message(message.chat.id,
                                        text=self.test_config.get("QUESTION", "question_" + str(self.current_question)))
            self.bot.register_next_step_handler(msg, self.save_answer)
        else:
            self.check_answers()
            self.test_result(message.chat.id)  # Сохраняет каждый ответ в список и вызывает функцию нового вопроса

    # Сохраняет каждый ответ в список и вызывает функцию нового вопроса
    def save_answer(self, message):
        self.answers.append(message.text)
        self.send_question(message)

    # Устанавливает число верных ответов
    def check_answers(self):
        for i in range(len(self.answers)):
            if self.answers[i] == self.test_config.get("ANSWERS", "answer_" + str(i + 1)):
                self.correct_answer += 1

    # Оповещает пользователя о результатах теста
    # todo дописать сюда функцию, которая будет вызывать метод из Processora, который запишет юзера прошедшего тест в БД
    def test_result(self, chat_id):
        if 3 > self.correct_answer >= 0:
            self.bot.send_message(chat_id, text=self.test_config.get("RESULT", "test_result_before") + " " + str(
                self.correct_answer) + " " + self.test_config.get("RESULT", "test_result_after") + self.test_config.get(
                "RESULT", "lox"))
        elif 5 > self.correct_answer >= 3:
            self.bot.send_message(chat_id, text=self.test_config.get("RESULT", "test_result_before") + " " + str(
                self.correct_answer) + " " + self.test_config.get("RESULT", "test_result_after") + self.test_config.get(
                "RESULT", "norm_lvl"))
        elif self.correct_answer >= 5:
            self.bot.send_message(chat_id, text=self.test_config.get("RESULT", "test_result_before") + " " + str(
                self.correct_answer) + " " + self.test_config.get("RESULT", "test_result_after") + self.test_config.get(
                "RESULT", "god"))

    # Создаёт кнопки ответа на тест
    def create_answer_button(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("1")
        btn2 = types.KeyboardButton("2")
        btn3 = types.KeyboardButton("3")
        btn4 = types.KeyboardButton("4")
        btn5 = types.KeyboardButton(self.config.get("DEFAULT", "main_menu") + "➡️")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        return markup

    # Функция которая создаёт кнопки главног меню
    def take_main_menu(self, message):
        markup = self.processor.create_start_button()
        self.bot.send_message(message.chat.id, self.config.get("DEFAULT", "main_menu") + "➡️", reply_markup=markup)
