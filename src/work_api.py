from abc import ABC, abstractmethod

import requests as requests


class WorkApi(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_info(self):
        pass


class HeadHunter(WorkApi):
    """Класс для работы с API HeadHunter"""

    url = 'https://api.hh.ru/vacancies'

    def __init__(self, text: str, per_page: int, city: int):
        self.text = text
        self.per_page = per_page
        self.area = city

    def get_info(self):
        """
        Получает список вакансий
        :return: list
        """
        response = requests.get(self.url, params=self.__dict__)
        info = response.json()['items']
        return info
