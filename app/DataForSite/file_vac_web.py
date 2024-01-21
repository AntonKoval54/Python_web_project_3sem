import pandas as pd
import datetime
import re
import requests
import xmltodict

filename = r"D:\Загрузки\vacancies_for_web.csv"
pd.set_option('display.max_columns', None)


valid_curr = ['ZAR', 'LVL', 'USD', 'JPY', 'AMD', 'XDR', 'TJS', 'GBP', 'AZN', 'SGD', 'BYR', 'TRL',
               'EGP', 'AED', 'CNY', 'UAH', 'CZK', 'AUD', 'EEK', 'KRW', 'NZD', 'SEK', 'THB', 'KGS',
               'CHF', 'PLN', 'KZT', 'IDR', 'NOK', 'LTL', 'QAR', 'ISK', 'UZS', 'EUR', 'VND', 'TRY',
               'HKD', 'BGN', 'DKK', 'GEL', 'BRL', 'RSD', 'HUF', 'RON', 'TMT', 'INR', 'MDL', 'CAD']

def get_date(x):
    original_date = datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S%z')
    new_date_str = original_date.strftime('%d/%m/%Y')
    new_date_str = '01'+new_date_str[2:]
    return new_date_str

def get_date_req(x):
    new_date_str = x.strftime('%Y-%m-%d')
    new_date_str = new_date_str[:8]+ '01'
    return new_date_str

def get_date_req_column(x):
    original_date = datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S%z')
    new_date_str = original_date.strftime('%d/%m/%Y')
    new_date_str = new_date_str[:8]+ '01'
    return new_date_str

def get_currency_rates_on_date(date):
    url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}"
    response = requests.get(url)
    if response.status_code == 200:
        data = xmltodict.parse(response.content)
        result = {'date': data['ValCurs']['@Date']}
        for elem in data['ValCurs']['Valute']:
            if elem['CharCode'] == "BYN":
                elem['CharCode'] = "BYR"
            result[elem['CharCode']] = elem['VunitRate']
        #result.insert(0,data['ValCurs']['@Date'])
        return result
    else:
        print("Ошибка при получении данных:", response.status_code, response.reason)
        return None

def get_pd_curr(earl, last):
    dates = pd.date_range(earl, last, freq='MS').strftime('%d/%m/%Y').tolist()
    # Получение курсов валют на каждую из этих дат
    currency_data = []
    for date in dates:
        rates = get_currency_rates_on_date(date)
        if rates:
            rates['date'] = date  # апи цб меняет иногда на 30 или 31 ну я думаю праздничные дни
            currency_data.append(rates)

    # Создание DataFrame
    df = pd.DataFrame(currency_data)

    # Вывод полученного DataFrame
    return df

# доделать по апи и сюда предеать огромный словари
# и умножить на коэф по дате
check_list = ['1с разработчик', '1c разработчик', '1с', '1c', '1 c', '1 с']
vacancies = pd.read_csv(filename)
vacancies=vacancies[vacancies['name'].str.contains('|'.join(check_list))]
vacancies['salary_from'] = vacancies['salary_from'].fillna(vacancies['salary_to'])
vacancies['salary_to'] = vacancies['salary_to'].fillna(vacancies['salary_from'])
vacancies['avg']=vacancies[['salary_from', 'salary_to']].mean(axis=1)
vacancies = vacancies.drop(['salary_from', 'salary_to'], axis=1)
time_for_mm = pd.to_datetime(vacancies['published_at'])
earliest_date = get_date_req(time_for_mm.min())
latest_date = get_date_req(time_for_mm.max())
#vacancies['date'] = vacancies['published_at'].apply(lambda x: get_date_req_column(x))
vacancies['date'] = vacancies['published_at'].apply(lambda x: get_date(x))
currency = get_pd_curr(earliest_date, latest_date)
#print(vacancies['salary_currency'].isin(["BYN"]).any())# false
#print(vacancies['salary_currency'].isin(["BYR"]).any())# true
result = vacancies.merge(currency, on=['date'])#inner join
print(result)
# print(earliest_date)
# print(latest_date)
# print(vacancies)