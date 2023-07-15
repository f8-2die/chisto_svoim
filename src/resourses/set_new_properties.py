import configparser

section = "DEFAULT"
option = "main_menu"
value = "В главное меню"


def wright(section, option, value):
    config = configparser.ConfigParser()

    path = "properties.ini"

    config.read(path)

    config.set(section, option, value)

    with open(path, "w") as f:
        config.write(f)


wright(section, option, value)
