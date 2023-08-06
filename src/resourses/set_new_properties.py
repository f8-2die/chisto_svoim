import configparser

section = "DEFAULT"
option = "test_already_is_over"
value = 'Тест уже был пройден! Если же менеджер так и не написал, скорее всего у тебя скрыт никнейм, пожалуйста, напиши нам сам ;)'


# programming = Программирование
# eng = Английский
# get_contact = Наши контакты


def wright(section, option, value):
    config = configparser.ConfigParser()

    path = "test.ini"

    config.read(path)

    config.set(section, option, value)

    with open(path, "w") as f:
        config.write(f)


wright(section, option, value)
