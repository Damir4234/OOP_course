import json
from abc import ABC, abstractmethod

import requests, os


class API_Connect(ABC):

    @abstractmethod
    def __init__(self, vacancies_url: str):
        self.vacancies_url = vacancies_url

    @abstractmethod
    def get_vacancies(self, keyword: str):
        pass


class Saver(ABC):

    @abstractmethod
    def __init__(self, name_of_file):
        self.name_of_file = name_of_file

    @abstractmethod
    def save_to_file(self):
        pass


class HeadHunterAPI(API_Connect):
    """
    Получает ключевое слово и делает запрос по API на площадку для поиска работы
    """

    def __init__(self):
        self.vacancies_url = "https://api.hh.ru/vacancies/"

    def get_vacancies(self, keyword: str):
        params = {
            "text": keyword,
            "per_page": 20,
        }
        response_HH = requests.get(self.vacancies_url, params=params)
        ids_HH = [item["id"] for item in response_HH.json()["items"]]
        dict_vacancies = {}
        for item_id in ids_HH:
            get_vac = requests.get(f"{self.vacancies_url}{item_id}").json()
            if get_vac["salary"] is None:
                salary_from = None
                salary_to = None
            else:
                salary_from = get_vac["salary"]["from"]
                salary_to = get_vac["salary"]["to"]
            dict_vacancies[item_id] = {"name": get_vac["name"], "salary from": salary_from,
                                       "salary to": salary_to, "url": get_vac["alternate_url"],
                                       "experience": get_vac["experience"]['name'], "tasks": get_vac["description"]}
        return dict_vacancies



