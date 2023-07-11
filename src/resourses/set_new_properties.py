import configparser

section = "KEY"
option = "api_key"
value = "6383973511:AAFMJBhyVwdV1PmNSfeT4zlycw3EsHNICTU"


def wright(section, option, value):
    config = configparser.ConfigParser()

    path = "api_key.ini"

    config.read(path)
    config.add_section("KEY")
    config.set(section, option, value)

    with open(path, "w") as f:
        config.write(f)


wright(section, option, value)
