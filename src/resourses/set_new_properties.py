import configparser

section = "DEFAULT"
option = "db_name"
value = "chisto_svoim_bd"


def wright(section, option, value):
    config = configparser.ConfigParser()

    path = "storage_config.ini"

    config.read(path)

    config.set(section, option, value)

    with open(path, "w") as f:
        config.write(f)


wright(section, option, value)
