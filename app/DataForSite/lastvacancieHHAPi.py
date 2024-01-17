import pandas as pd
import datetime
import re
import requests

money_name = {"AZN": "Манаты", "BYR": "Белорусские рубли", "EUR": "Евро", "GEL": "Грузинский лари",
              "KGS": "Киргизский сом", "KZT": "Тенге", "RUR": "Рубли", "UAH": "Гривны", "USD": "Доллары",
              "UZS": "Узбекский сум", None: "валюта не указана"}
def get_lact_vac():
    profession = "1С программист"  # Профессия, по которой будет выполняться поиск
    industry = 96 # прогеры у hh такой id
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat()  # Дата и время 24 часа назад

    # Выполняем GET-запрос для получения списка вакансий по конкретной профессии за последние 24 часа
    #response = requests.get(f'https://api.hh.ru/vacancies?text={profession}&professional_role=96&date_from={yesterday}&date_to={today}')
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': 'NAME:(1С программист)',
        'date_from': f'{yesterday}',
        'professional_role': '96'
    }
    response = requests.get(url, params=params)
    # Проверяем успешность запроса
    if response.status_code == 200:
        vacancies = response.json()

        if vacancies['found'] > 0:
            result = []
            for vacancy in vacancies['items'][:10]:
                vacancy_id = vacancy['id']
                # Получаем подробную информацию о вакансии
                vacancy_info_response = requests.get(f'https://api.hh.ru/vacancies/{vacancy_id}')
                if vacancy_info_response.status_code == 200:
                    vacancy_info = vacancy_info_response.json()

                    # Извлекаею данные о вакансии
                    vacancy_title = vacancy_info['name']
                    temp = re.sub(r'<.*?>', "", vacancy_info['description'])
                    vac_description = ' '.join(temp.strip().split())
                    skills = ",".join(skill['name'] for skill in vacancy_info.get('key_skills', []))
                    if len(skills)==0:
                        skills = "( работодатель не указал навыки :/ )"
                    company_name = vacancy_info['employer']['name']
                    salary = vacancy_info['salary']
                    if salary is None:
                        salary = {"currency":"з/п не указана"}
                    if 'to' in salary and salary['to'] is None:
                        del salary['to']
                    if 'from' in salary and salary['from'] is None:
                        del salary['from']
                    if salary['currency'] in money_name:
                        salary['currency'] = money_name[salary['currency']]
                    region_name = vacancy_info['area']['name']
                    publication_date = re.sub("([0-9]{4})-([0-9]{2})-([0-9]{2})", r"\3.\2.\1", vacancy_info['published_at'].split("T")[0])
                    vac_dct = {
                        "name": vacancy_title,
                        "description" : vac_description,
                        "skills" : skills,
                        "company" : company_name,
                        "salary" : salary,
                        "region_name": region_name,
                        "published_at": publication_date,
                    }

                    result.append(vac_dct)
            return result
        else:
            return ["Вакансий по данной профессии за последние 24 часа не найдено"]
    else:
        return[f" Что пошло не так  - Ошибка {response.status_code}: {response.reason}"]