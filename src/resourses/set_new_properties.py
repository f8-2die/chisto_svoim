import configparser

section = "RESPONSE"
option = "eng_test_response"
value = "Итак, приступим к написанию теста, который поможет понять полный ты дуб или нет :)"


def wright(section, option, value):
    config = configparser.ConfigParser()

    path = "properties.ini"

    config.read(path)

    config.set(section, option, value)

    with open(path, "w") as f:
        config.write(f)


wright(section, option, value)
