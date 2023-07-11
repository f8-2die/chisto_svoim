import configparser

section = "KEY"
option = "api_key"
value = ""


def wright(section, option, value):
    config = configparser.ConfigParser()

    path = "api_key.ini"

    config.read(path)

    config.set(section, option, value)

    with open(path, "w") as f:
        config.write(f)


wright(section, option, value)
