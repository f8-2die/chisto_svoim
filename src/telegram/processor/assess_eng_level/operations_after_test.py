import configparser

from src.errors.errors import Failed_execution_test
from src.logic.eng.estimation.preporation_befor_save_bd import Preparation_before_save_bd
from src.telegram.processor.assess_eng_level.testing import Test


class Operations_after_test:
    errors_config = configparser.ConfigParser()
    errors_config.read("src/resourses/errors_text.ini")

    '''
    Метод с задержкой в 2 минуты вызывает следующие методы: 
    1) Проверку завершён ли тест экстренно или же нормально
    2) Если нормально, то запускает обработку результатов и подготовку их для записи в БД
    3) Записывает в БД
    4) Пишет преподам, что тест был пройден
    '''

    def __init__(self, bot, processor, loger):
        self.loger = loger
        self.bot = bot
        self.processor = processor

    def processing_save_user(self, message):
        try:
            test = Test(self.bot, self.processor.storage, self.loger)  # создаёт экземпляр теста
            test.assess_eng_level(message)  # запускает метод с началом теста
            preparation_before_save_bd = Preparation_before_save_bd(test,
                                                                    message,
                                                                    self.loger)  # экземпляр класса с обработкой результатов
            preparation_before_save_bd.run_after_delay(20,
                                                       preparation_before_save_bd.checking_test_completion)  # проверяет закончен ли тест
            preparation_before_save_bd.run_after_delay(22,
                                                       preparation_before_save_bd.result_processing_if_test_is_over)  # обрабатывает результаты, если они не были обработаны
            preparation_before_save_bd.run_after_delay(23, preparation_before_save_bd.get_user)  # получает юзера
            preparation_before_save_bd.run_after_delay(24,
                                                       preparation_before_save_bd.checking_existence_user)  # проверяет существование юзера в БД
            preparation_before_save_bd.run_after_delay(25,
                                                       preparation_before_save_bd.save_new_user)  # сохраняет юзера в бд
            preparation_before_save_bd.run_after_delay(26,
                                                       preparation_before_save_bd.get_all_teacher)  # получает список преподов
            preparation_before_save_bd.run_after_delay(27,
                                                       preparation_before_save_bd.send_message_teachers)  # отправляет преподам сообщение о завершении теста юзером
        except Failed_execution_test as e:
            print(self.errors_config.get("Events_errors", "failed_execute_test") + str(e))
