import configparser

section = "DEFAULT"
option = "start_message"
value = 'Привет!\nЯ тг-бот проекта "Чисто своим!"\nЛистай меню и посмотри, что я умею!'


def wright(section, option, value):
    config = configparser.ConfigParser()

    config.read("properties.ini")

    config.set(section, option, value)

    with open("properties.ini", "w") as f:
        config.write(f)


wright(section, option, value)
