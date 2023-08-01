from abc import ABC
import json


class WorkToFile(ABC):
    """
    Абстрактный класс для работы с файлами
    """
    @staticmethod
    def read():
        pass

    @staticmethod
    def write():
        pass


class ReadWriteToJSON(WorkToFile):
    """
    Класс для работы с JSON-файлами
    """
    @staticmethod
    def read_json(file_name='vacancies.json'):
        """
        Чтения JSON-файла
        :return: list
        """
        with open(file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data

    @staticmethod
    def write_json(data, file_name='vacancies.json'):
        """
        Записи информации в JSON-файл
        """
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    @staticmethod
    def add_json(data):
        """
        Добавления информации в JSON-файл
        """
        all_data = ReadWriteToJSON.read_json()
        for i in data:
            all_data.append(i)
        with open('vacancies.json', 'w', encoding='utf-8') as file:
            json.dump(all_data, file, indent=4, ensure_ascii=False)


class ReadWriteToSQL:
    """
    Класс для записи SQL запросов
    """

    @staticmethod
    def read_sql(file_name='queries.sql'):
        """
        Чтения SQL-файла
        :return: str
        """
        with open(file_name, 'r', encoding='utf-8') as file:
            data = file.read()
            return data

    @staticmethod
    def add_info(data, file_name='queries.sql'):
        """
        Добавления информации в SQL-файл
        """

        with open(file_name, 'a', encoding='utf-8') as file:
            file.write(data)
