import pandas as pd
import datetime
import re
import requests

# Параметры запроса
profession = "1С программист"  # Профессия, по которой будет выполняться поиск
industry = 96 # прогеры у hh такой id
today = datetime.datetime.now().isoformat()  # Текущая дата и время
yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat()  # Дата и время 24 часа назад

# Выполняем GET-запрос для получения списка вакансий по конкретной профессии за последние 24 часа
#response = requests.get(f'https://api.hh.ru/vacancies?text={profession}&professional_role=96&date_from={yesterday}&date_to={today}')
url = 'https://api.hh.ru/vacancies'
params = {
    'text': 'NAME:(1С)',
    'date_from': f'{yesterday}',
    'professional_role': '96'
}
response = requests.get(url, params=params)
# Проверяем успешность запроса
if response.status_code == 200:
    vacancies = response.json()

    if vacancies['found'] > 0:
        for vacancy in vacancies['items'][:10]:
            vacancy_id = vacancy['id']

            # Получаем подробную информацию о вакансии
            vacancy_info_response = requests.get(f'https://api.hh.ru/vacancies/{vacancy_id}')
            if vacancy_info_response.status_code == 200:
                vacancy_info = vacancy_info_response.json()

                # Извлекаем необходимые данные о вакансии
                vacancy_title = vacancy_info['name']
                temp = re.sub(r'<.*?>', "", vacancy_info['description'])
                vacancy_description = ' '.join(temp.strip().split())
                skills = ",".join(skill['name'] for skill in vacancy_info.get('key_skills', []))
                company_name = vacancy_info['employer']['name']
                salary = vacancy_info['salary']
                region_name = vacancy_info['area']['name']
                publication_date = vacancy_info['published_at']

                # Выводим данные о вакансии
                print(f"Название вакансии: {vacancy_title}")
                print(f"Описание вакансии: {vacancy_description}")
                print(f"Навыки: {skills}")
                print(f"Компания: {company_name}")
                print(f"Оклад: {salary}")
                print(f"Название региона: {region_name}")
                print(f"Дата публикации вакансии: {publication_date}")
    else:
        print("Вакансий по данной профессии за последние 24 часа не найдено")

else:
    print(f"Ошибка {response.status_code}: {response.reason}")