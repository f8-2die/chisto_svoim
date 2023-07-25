import configparser

section = "MESSAGE_TO_TEACHER"
option = "complete_test"
value = " только что прошёл тест со следующими ошибками: "


def wright(section, option, value):
    config = configparser.ConfigParser()

    path = "test.ini"

    config.read(path)
    config.set(section, option, value)

    with open(path, "w") as f:
        config.write(f)


wright(section, option, value)
