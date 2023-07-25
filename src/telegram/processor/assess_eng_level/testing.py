import configparser
from telebot import types

from src.logic.eng.estimation.estimation import Test_estimation
from src.telegram.processor.processor import Processor

"""
    Класс отвечает за проведение теста пользователя.
    Он умеет задавать вопросы, запоминать ответы на эти вопросы
    И умеет выводить результат
"""


class Test(Processor):
    current_question = 0  # Номер текущего вопроса
    correct_answer = 0  # Количество правильных ответов
    answers = []  # Список с ответами пользователя
    incorrect_answers = {}
    end_test = False

    def __init__(self, bot, storage):
        self.bot = bot
        self.storage = storage
        super().__init__(self.bot, self.storage)

    def __set__(self):
        self.incorrect_answers()

    config = configparser.ConfigParser()
    config.read("src/resourses/properties.ini")

    test_config = configparser.ConfigParser()
    test_config.read("src/resourses/test.ini")

    # Отправка сообщения о том, что тест начинается
    def offer_take_test(self, message, markup):
        self.bot.send_message(message.chat.id, text=self.config.get("RESPONSE", "eng_test_response"),
                              reply_markup=markup)

    # Старт теста
    def start_test(self):
        self.answers = []
        self.current_question = 0
        self.correct_answer = 0

    """
        Проверяет, есть ли запрос на выход из теста 
        Затем, если число отправленных вопросов меньше количества вопросов,то отправляет вопрос 
        Если число отправленных вопросов и общее их число равно, то вызывает функцию проверки результата и функцию 
        оповещения о результате пользователя.
    """

    def send_question(self, message):
        if message.text == self.config.get("DEFAULT", "main_menu") + "➡️":
            self.take_main_menu(message)
            self.end_test = True
            return
        self.current_question += 1
        if self.current_question < int(self.test_config.get("DEFAULT", "questions_score")):
            msg = self.bot.send_message(message.chat.id,
                                        text=self.test_config.get("QUESTION", "question_" + str(self.current_question)))
            self.bot.register_next_step_handler(msg, self.save_answer)
        else:
            self.result_processing(message)

    '''
    Вызывает класс, который обработает результат
    Затем вызывает методы этого класса
    Отсылает юзеру результаты 
    Выходит в главное меню
    '''

    def result_processing(self, message):
        test_estimation = Test_estimation(
            self.answers)  # создаёт класс, который будет оценивать результаты и их передаёт
        test_estimation.check_answers()  # подсчитывает количество верных ответов
        self.correct_answer = test_estimation.correct_answer
        self.incorrect_answers = test_estimation.incorrect_answers
        level = test_estimation.result_processing()  # выдаёт результат
        self.send_results_to_user(message.chat.id, level)
        self.take_main_menu(message)

    # Сохраняет каждый ответ в список и вызывает функцию нового вопроса
    def save_answer(self, message):
        self.answers.append(message.text)
        self.send_question(message)

    # Оповещает пользователя о результатах теста
    def send_results_to_user(self, chat_id, level):
        if level == "low_level":
            self.bot.send_message(chat_id, text=self.test_config.get("RESULT", "test_result_before") + " " + str(
                self.correct_answer) + " " + self.test_config.get("RESULT", "test_result_after") + self.test_config.get(
                "RESULT", "lox"))
        elif level == "medium_level":
            self.bot.send_message(chat_id, text=self.test_config.get("RESULT", "test_result_before") + " " + str(
                self.correct_answer) + " " + self.test_config.get("RESULT", "test_result_after") + self.test_config.get(
                "RESULT", "norm_lvl"))
        elif level == "height_level":
            self.bot.send_message(chat_id, text=self.test_config.get("RESULT", "test_result_before") + " " + str(
                self.correct_answer) + " " + self.test_config.get("RESULT", "test_result_after") + self.test_config.get(
                "RESULT", "god"))
            # todo прописать ошибку в else

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
        markup = self.create_start_button()
        self.bot.send_message(message.chat.id, self.config.get("DEFAULT", "main_menu") + "➡️", reply_markup=markup)

    """
    Вызывает методы, которые сначала задают вопросы юзеру
    А затем оценивают результат теста
    Затем же озвучивают результат теста
    """

    def assess_eng_level(self, message):
        markup = self.create_answer_button()
        self.offer_take_test(message, markup)  # пишет юзеру что тест начался
        self.start_test()  # запускает тест
        self.send_question(message)  # задаёт первый вопрос
