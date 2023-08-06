"""
Отвечает за какие-либо ошибки
"""
import configparser
import logging
from datetime import datetime


class Failed_save_user(Exception):
    pass


class Failed_get_teachers(Exception):
    pass


class Failed_start_test_passing_with_new_thread(Exception):
    pass


class Failed_send_anik(Exception):
    pass


class Failed_send_contact(Exception):
    pass


class Failed_create_main_menu_buttons(Exception):
    pass


class Failed_start_message(Exception):
    pass


class Failed_execution_test(Exception):
    pass


class Failed_send_helloMessage_to_user(Exception):
    pass


class Failed_create_start_button(Exception):
    pass


class Failed_send_offer_take_test(Exception):
    pass


class Failed_send_question_eng_test(Exception):
    pass


class Failed_process_test_result(Exception):
    pass


class Failed_send_test_result_to_user(Exception):
    pass


class Failed_create_test_button(Exception):
    pass


class Failed_send_message_to_teacher(Exception):
    pass


class Failed_run_after_delay_in_new_threading(Exception):
    pass


class Failed_connect_bd(Exception):
    pass


class Failed_get_user(Exception):
    def __init__(self, e):
        logging.basicConfig(level=logging.ERROR, filename="popa.log", filemode="w", encoding='utf-8')
        loger = logging.getLogger("loger")
        errors_config = configparser.ConfigParser()
        errors_config.read("src/resourses/errors_text.ini")
        self.loger = loger
        self.errors_config = errors_config
        self.e = e
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.loger.error(current_time + self.errors_config.get("Database_errors", "failed_get_user") + str(e))

