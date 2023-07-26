import configparser

section = "Database_errors"
option = "failed_open_db_connect"
value = 'Не удалось открыть соединение с БД: '


def wright(section, option, value):
    config = configparser.ConfigParser()

    path = "errors_text.ini"

    config.read(path)
    config.set(section, option, value)

    with open(path, "w") as f:
        config.write(f)


wright(section, option, value)
