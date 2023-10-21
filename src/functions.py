import requests


def get_id(city):
    """Функция залезет в файл areas.json и по искомому городу
    найдет его id (проверено только на больших городах)"""
    # Загружаю список:
    response = requests.get('https://api.hh.ru/areas')
    response_json = response.json()
    response_json = str(response_json)
    # Ищу по какому адресу находится данное слово
    search_data = response_json.find(city)
    # Отрезаю кусок строки с искомым словом так, чтобы в кусок уместилось id
    city_data = response_json[search_data-45: search_data+20]
    # Еще сильнее урезаю строку так, чтобы в строке остался только id
    id_data = city_data.find('id')
    number_str = city_data[id_data: id_data + 11]
    # Перебераю строку,чтобы сохранить только номер:
    number = ''
    for letter in number_str:
        if letter.isdigit():
            number += letter
    try:
        return int(number)
    except ValueError:
        print('Упс! Что-то пошло не так...Попробуйте снова.')
