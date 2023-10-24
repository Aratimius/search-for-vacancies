from src.get_api import HeadHunter, SuperJob
from src.work_api import WorkWithVacancies


def lets_go():
    print("""Программа для поиска и обработки данных по вакансиям.
    1 - поиск вакансии на hh.ru
    2 - поиск вакансий на Superjob
    3 - поиск вакансий на hh.ru и Superjob
    0 - выход
После того, как вы определились с тем, на какой платформе будете искать:
    'show' - показать найденные вакансии в консоли
    'save' - сохранить вакансии в файл
    'sort' - сортировать вакансии (1 - по зарплате, 2 - по дате публикации)
    0 - вернуться обратно к выбору платформы по поиску вакансий""")

    while True:
        platform_input = int(input('Где будем искать?: '))
        if platform_input == 0:
            break
        header = None
        vacancies = None
        if platform_input == 1:
            header = 'Поиск на hh.ru:'
            print(header)
            text = input('Введите ключевое слово: ')
            area = input('Введите город: ')
            per_page = int(input('Введите максимальное число вакансий: '))
            hh = HeadHunter(text, area, per_page)
            vacancies = WorkWithVacancies(hh)
        elif platform_input == 2:
            header = 'Поиск на Superjob.ru:'
            print(header)
            text = input('Введите ключевое слово: ')
            area = input('Введите город: ')
            per_page = int(input('Введите максимальное число вакансий: '))
            superjob = SuperJob(text, area, per_page)
            vacancies = WorkWithVacancies(superjob)
        elif platform_input == 3:
            header = 'Поиск на Superjob.ru и hh.ru:'
            print(header)
            text = input('Введите ключевое слово: ')
            area = input('Введите город: ')
            per_page = int(input("""Введите максимальное число вакансий, c hh и superjob
(если, к примеру, вы вводите одну вакансию, то придет одна ваканчия с hh и одна c Superjob): """))
            superjob = SuperJob(text, area, per_page)
            hh = HeadHunter(text, area, per_page)
            vacancies = WorkWithVacancies(superjob, hh)
        else:
            print('Нет такой функции')
        while True:
            print(header, '\n', """'show' - показать найденные вакансии в консоли
 'save' - сохранить вакансии в файл
 'sort' - сортировать вакансии (1 - по зарплате, 2 - по дате публикации)
 0 - вернуться обратно к выбору платформы по поиску вакансий""")
            actions_input = input('Ваши действия: ')
            if actions_input == 'save':
                filename = input('В какой файл сохранить ваканчии?: ')
                vacancies.save_vacancies(filename)
            elif actions_input == 'show':
                vacancies.show_vacancies()
            elif actions_input == 'sort':
                sort_input = int(input('1 - по зарплате, 2 - по дате публикации: '))
                if sort_input == 1:
                    vacancies.get_sorted('payment_from')
                elif sort_input == 2:
                    vacancies.get_sorted('published_date')
                else:
                    print('Нет такой функции')
            elif actions_input == '0':
                break
            else:
                print('Нет такой функции')


if __name__ == '__main__':
    lets_go()
