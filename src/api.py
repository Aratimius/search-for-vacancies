import json
from abc import ABC, abstractmethod
import requests
from datetime import datetime
from .functions import get_id  # точка означает, что я к этой функции буду обращаться в main, что лежит на каталог выше


class API(ABC):
    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunter(API):
    """Класс для работы с API hh.ru"""
    def __init__(self, text: str, area: str, per_page: int) -> None:
        self.text = text
        self.id = get_id(area)
        self.per_page = per_page
        self.vacancies = self.get_vacancies()

    def __add__(self, other):
        return self.vacancies + other.vacancies

    def get_vacancies(self):
        """Вернет словарь с данными с сайта hh.ru"""
        params = {
            'text': self.text,
            'area': self.id,
            'per_page': self.per_page
        }
        response = requests.get('https://api.hh.ru/vacancies', params=params)
        response_json = response.json()
        return_data = []
        for data in response_json['items']:
            new_data = {'profession': data['name'], 'city': data['area']['name'],
                        'published_date': data['published_at']
                        }
            # Не у всех вакансий есть url, а мне хотелось бы отслеживать url:
            if 'url' in data.keys():
                new_data['url'] = data['url']
            return_data.append(new_data)
            # Та же история с зарплатой, там вообще мрак:
            if 'salary' in data.keys() and isinstance(data['salary'], dict)\
                    and data['salary'] is not None and data['salary']['from'] is not None:
                new_data['payment_from'] = data['salary']['from']
            else:
                new_data['payment_from'] = 0
        return return_data


class SuperJob(API):
    """Класс для работы с API Superjob.ru"""
    def __init__(self, keyword: str, town: str, per_page: int) -> None:
        self.keyword = keyword
        self.town = town
        self.per_page = per_page  # максимальное колличество вакансий, которое хочет видеть пользователь
        self.vacancies = self.get_vacancies()

    def __add__(self, other):
        return self.vacancies + other.vacancies

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
        # Нужен счетчик для того, чтобы ограничить колличество записанных вакансий
        count = self.per_page
        return_data = []
        for data in response_json['objects']:
            # Для начала переделаем дату под нужный нам формат:
            data['date_published'] = str(datetime.fromtimestamp(data['date_published']))
            data['date_published'] = data['date_published'].replace(' ', 'T')
            # Теперь достаем нужные нам данные:
            new_data = {'profession': data['profession'], 'city': data['town']['title'],
                        'published_date': data['date_published'], 'payment_from': data['payment_from']}
            if 'url' in data['client'].keys():
                new_data['url'] = data['client']['url']
            return_data.append(new_data)
            count -= 1
            if count == 0:
                break
        return return_data


class WorkWithAPI(ABC):
    @abstractmethod
    def save_vacancies(self):
        pass


class WorkWithVacancies:
    def __init__(self, vacancies):
        super().__init__()
        self.vacancies = vacancies

    def show_vacancies(self):
        """Выводит вакасии в терминал"""
        for vacancy in self.vacancies:
            print(vacancy)

    def get_sorted(self, vacancies_key):
        """Сортирует вакансии по заданному ключу"""
        self.vacancies = sorted(self.vacancies, key=lambda operation: operation[vacancies_key], reverse=True)


class WorkWithSuperjob(WorkWithVacancies, WorkWithAPI):
    """Класс для обработки данных по вакансиям с Superjob"""
    def __init__(self, vacancies):
        super().__init__(vacancies)
        self.vacancies = vacancies.vacancies

    def save_vacancies(self):
        """Сохраняет вакансии в файл"""
        to_save = None
        while to_save not in ['Y', 'N']:
            to_save = input('Вы хотите сохранить вакансии в файл?[Y/N]: ')
            if to_save == 'Y':
                with open('superjob.json', 'w') as file:
                    json.dump(self.vacancies, file, sort_keys=True, ensure_ascii=False)
                    print('Вакансии сохранены')
            elif to_save == 'N':
                print('Вакансии не сохранены в superjob.json')
            else:
                print('Нужно ввести N-нет или Y-да')


class WorkWithHH(WorkWithVacancies, WorkWithAPI):
    """Класс для обработки данных по вакансиям с hh.ru"""
    def __init__(self, vacancies):
        super().__init__(vacancies)
        self.vacancies = vacancies.vacancies

    def save_vacancies(self):
        """Сохраняет вакансии в файл"""
        to_save = None
        while to_save not in ['Y', 'N']:
            to_save = input('Вы хотите сохранить вакансии в файл?[Y/N]: ')
            if to_save == 'Y':
                with open('hh.json', 'w') as file:
                    json.dump(self.vacancies, file, sort_keys=True, ensure_ascii=False)
                    print('Вакансии сохранены')
            elif to_save == 'N':
                print('Вакансии не сохранены в hh.json')
            else:
                print('Нужно ввести N-нет или Y-да')


class WorkWithAll(WorkWithVacancies, WorkWithAPI):
    """Класс для обработки данных по всем вакансиям"""
    def __init__(self, vacancies, other_vacancies):
        super().__init__(vacancies)
        self.vacancies = vacancies + other_vacancies

    def save_vacancies(self):
        """Сохраняет вакансии в файл"""
        to_save = None
        while to_save not in ['Y', 'N']:
            to_save = input('Вы хотите сохранить вакансии в файл?[Y/N]: ')
            if to_save == 'Y':
                with open('all_vacancies.json', 'w') as file:
                    json.dump(self.vacancies, file, sort_keys=True, ensure_ascii=False)
                    print('Вакансии сохранены all_vacancies.json')
            elif to_save == 'N':
                print('Вакансии не сохранены')
            else:
                print('Нужно ввести N-нет или Y-да')

