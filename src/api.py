import json
from abc import ABC, abstractmethod
import requests


class API(ABC):
    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunter(API):
    """Класс для работы с API hh.ru"""
    def __init__(self, text: str, area: int, per_page: int) -> None:
        self.text = text
        self.area = area
        self.per_page = per_page
        self.vacancies = self.get_vacancies()

    def get_vacancies(self):
        """Вернет словарь с данными с сайта hh.ru"""
        params = {
            'text': self.text,
            'area': self.area,
            'per_page': self.per_page
        }
        response = requests.get('https://api.hh.ru/vacancies', params=params)
        response_json = response.json()
        return_data = []
        for data in response_json['items']:
            new_data = {'profession': data['name'], 'city': data['area']['name'],
                        'published date': data['published_at'], 'payment_from': data['salary']['from']}
            if 'url' in data.keys():
                new_data['url'] = data['url']
            return_data.append(new_data)
        return return_data


class SuperJob(API):
    """Класс для работы с API Superjob.ru"""
    def __init__(self, keyword: str, town: str) -> None:
        self.keyword = keyword
        self.town = town
        self.vacancies = self.get_vacancies()

    def get_vacancies(self):
        """Вернет словарь с данными с сайта hh.ru"""
        headers = {'X-Api-App-Id': 'v3.r.137881293.aba1d41b86fd649e24217c1d1642573ee1ec909c.557356da2c9370a3391dd02d1bb7d4d7f339f34e'
                   }
        params = {
            'keywords': self.keyword,
            'town': self.town
        }
        response = requests.get('https://api.superjob.ru/2.0/vacancies', params=params, headers=headers)
        response_json = response.json()
        return_data = []
        for data in response_json['objects']:
            new_data = {'profession': data['profession'], 'city': data['town']['title'],
                        'published date': data['date_published'], 'payment_from': data['payment_from']}
            if 'url' in data['client'].keys():
                new_data['url'] = data['client']['url']
            return_data.append(new_data)
        return return_data


class WorkWithAPI(ABC):
    @abstractmethod
    def save_vacancies(self):
        pass


class WorkWithSuperjob(WorkWithAPI):
    """Класс для обработки данных по вакансиям с Superjob"""
    def __init__(self, superjob):
        self.superjob = superjob

    def save_vacancies(self):
        """Сохраняет вакансии в файл"""
        to_save = None
        while to_save not in ['Y', 'N']:
            to_save = input('Вы хотите сохранить вакансии в файл?[Y/N]: ')
            if to_save == 'Y':
                with open('superjob.json', 'w') as file:
                    json.dump(self.superjob.vacancies, file, sort_keys=True, ensure_ascii=False)
                    print('Вакансии сохранены')
            elif to_save == 'N':
                print('Вакансии не сохранены')
            else:
                print('Нужно ввести N-нет или Y-да')


class WorkWithHH(WorkWithAPI):
    """Класс для обработки данных по вакансиям с hh.ru"""
    def __init__(self, hh):
        self.hh = hh

    def save_vacancies(self):
        """Сохраняет вакансии в файл"""
        to_save = None
        while to_save not in ['Y', 'N']:
            to_save = input('Вы хотите сохранить вакансии в файл?[Y/N]: ')
            if to_save == 'Y':
                with open('hh.json', 'w') as file:
                    json.dump(self.hh.vacancies, file, sort_keys=True, ensure_ascii=False)
                    print('Вакансии сохранены')
            elif to_save == 'N':
                print('Вакансии не сохранены')
            else:
                print('Нужно ввести N-нет или Y-да')

