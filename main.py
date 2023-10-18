from src.api import HeadHunter, SuperJob, WorkWithHH, WorkWithSuperjob


# name = input('Введите специальность: ')
# number = int(input('Введите колличество страниц: '))
# city_id = int(input('Введите id города: '))

hh_ru = HeadHunter('python developer', 'Санкт-Петербург', 5)
print(hh_ru.id)
# superjob = SuperJob('python-разработчик', 'Санкт-Петербург', 2)

# save = WorkWithSuperjob(superjob)
# save.save_vacancies()
save = WorkWithHH(hh_ru)
save.save_vacancies()
