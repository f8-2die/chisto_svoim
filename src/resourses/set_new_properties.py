import configparser

section = "MESSAGE_TO_TEACHER"
option = "complete_test_null_errors"
value = ' прошёл тест без ошибок! Скорее пиши этому гению ;)'


def wright(section, option, value):
    config = configparser.ConfigParser()

    path = "test.ini"

    config.read(path)
    config.set(section, option, value)

    with open(path, "w") as f:
        config.write(f)


wright(section, option, value)
