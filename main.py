from src.api import HeadHunter, SuperJob, WorkWithHH, WorkWithSuperjob


# name = input('Введите специальность: ')
# number = int(input('Введите колличество страниц: '))
# city_id = int(input('Введите id города: '))

# hh_ru = HeadHunter('python developer', 2, 5)
superjob = SuperJob('python-разработчик', 'Санкт-Петербург')

save = WorkWithSuperjob(superjob)
save.save_vacancies()
