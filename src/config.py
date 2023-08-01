from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    """
    Создаёт словарь с данными для подключения к базе данных
    :param filename: str
    :param section: str
    :return: dict
    """
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db
