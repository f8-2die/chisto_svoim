"""
Этот модуль отвечает за логику оценки знаний
"""
import configparser


class Test_estimation:
    def __init__(self, answers, loger):
        self.loger = loger
        self.correct_answer = 0
        self.incorrect_answers = {}
        self.answers = answers

    test_config = configparser.ConfigParser()
    test_config.read("src/resourses/test.ini")



    # Устанавливает число верных ответов
    def check_answers(self):
        for i in range(len(self.answers)):
            if self.answers[i] == self.test_config.get("ANSWERS", "answer_" + str(i + 1)):
                self.correct_answer += 1
            else:
                self.incorrect_answers[self.test_config.get("QUESTIONS_WITHOUT_ANSWERS", "question_" + str(i + 1))] = \
                self.answers[i]
