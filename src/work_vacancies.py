import re
from abc import ABC, abstractmethod
import datetime


class Vacancies(ABC):
    """
    Абстрактный класс для вакансий
    """
    @abstractmethod
    def __init__(self):
        pass


class VacanciesHH(Vacancies):
    """
    Класс для работы с вакансиями HeadHunter
    """
    def __init__(self, info):
        self.url = info['alternate_url']
        self.company = info['employer']['name']
        self.title = info['name']
        self.city = info['area']['name']
        if info['salary'] == None:
            self.salary_int = 0
            self.salary = 'Зарплата не указана'
        else:
            if info['salary']['from'] != None:
                self.salary_int = info['salary']['from']
                self.salary = f"Зарплата от {info['salary']['from']} {info['salary']['currency']}"
            else:
                self.salary_int = info['salary']['to']
                self.salary = f"Зарплата до {info['salary']['to']} {info['salary']['currency']}"
        info_requirements = f"{info['snippet']['requirement']} {info['snippet']['responsibility']}"
        self.requirements = f"{self.clean_html(info_requirements)}"
        self.date = self.date_convesion(info['created_at'])

    @staticmethod
    def date_convesion(data):
        """
        Конвертирует дату в читаемый вид
        :param data: str
        :return: str
        """
        data_format = datetime.datetime.strptime(data, '%Y-%m-%dT%H:%M:%S%z')
        return f"Дата создания вакансии: {datetime.datetime.strftime(data_format, '%d %B %Y %H:%M:%S %Z')}"

    @staticmethod
    def clean_html(raw_html):
        clean_r = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        cleantext = re.sub(clean_r, '', raw_html)
        return cleantext
