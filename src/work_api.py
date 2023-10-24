import json
from abc import ABC, abstractmethod


class WorkWithAPI(ABC):
    @abstractmethod
    def save_vacancies(self, filename: str):
        pass


class WorkWithVacancies(WorkWithAPI):
    """Класс для обработки данных по вакансиям"""
    def __init__(self, *args):
        if len(args) > 1:
            self.vacancies = args[0] + args[1]
        else:
            self.vacancies = args[0].vacancies

    def save_vacancies(self, filename: str):
        """Сохраняет вакансии в файл"""
        to_save = None
        while to_save not in ['Y', 'N']:
            to_save = input('Вы хотите сохранить вакансии в файл?[Y/N]: ')
            if to_save == 'Y':
                with open(filename, 'w') as file:
                    json.dump(self.vacancies, file, sort_keys=True, ensure_ascii=False)
                    print(f'Вакансии сохранены в {filename}')
            elif to_save == 'N':
                print('Вакансии не сохранены')
            else:
                print('Нужно ввести N-нет или Y-да')

    def show_vacancies(self):
        """Выводит вакасии в терминал"""
        for vacancy in self.vacancies:
            print(vacancy)

    def get_sorted(self, vacancies_key):
        """Сортирует вакансии по заданному ключу"""
        self.vacancies = sorted(self.vacancies, key=lambda operation: operation[vacancies_key], reverse=True)
