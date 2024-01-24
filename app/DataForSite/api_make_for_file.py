import numpy as np
import pandas as pd
from make_file import get_currency_in_rur
import datetime
import json


def prepare_df(df: pd.DataFrame):
    df["salary"] = df[['salary_from', 'salary_to']].mean(axis=1)
    df["salary"] = df.apply(
        lambda row: np.nan if pd.isnull(row["salary_currency"]) else
        row["salary"] * get_currency_in_rur(str(row["salary_currency"]), str(row["published_at"])), axis=1
    )
    #елси зп нет nan иначе переводим
    df = df.drop(df[df["salary"] >= 10000000.0].index)
    df["published_year"] = pd.to_datetime(df["published_at"], utc=True).dt.year#только год
    return df


def get_demand_page_content(df: pd.DataFrame):
    # Страница Востребованность
    # Динамика уровня зарплат по годам
    salaries_dynamics = df.groupby("published_year")["salary"].mean().astype(int).to_dict()
    print(f"Динамика уровня зарплат по годам: {salaries_dynamics}")

    vacancies_dynamics = df['published_year'].value_counts().sort_index().astype(int).to_dict()
    print(f"Динамика количества вакансий по годам: {vacancies_dynamics}")

    # Динамика зарплат по годам для выбранной профессии
    data_prof = df[df['name'].str.contains(profession_name, case=False, na=False)]
    prof_salaries_dynamics = data_prof.groupby("published_year")["salary"].mean().astype(int).to_dict()
    print(f"Динамика зарплат по годам для выбранной профессии: {prof_salaries_dynamics}")

    # Доля вакансий по годам для выбранной профессии
    prof_vacancies_dynamics = data_prof["published_year"].value_counts().sort_index().astype(int).to_dict()
    print(f"Динамика вакансий по годам для выбранной профессии {prof_vacancies_dynamics}")


def get_geography_page_content(df: pd.DataFrame):
    # Страница География
    # Фильтрация 0.2%
    total_vacancies = df.shape[0]
    min_vacancies_threshold = total_vacancies * 0.002
    filtered_cities = df['area_name'].value_counts()
    filtered_cities = filtered_cities[filtered_cities >= min_vacancies_threshold]

    # Доля вакансий по городам (в порядке убывания)
    vacancies_by_area = df['area_name'].value_counts(normalize=True)
    vacancies_by_area = vacancies_by_area[
        vacancies_by_area.index.isin(filtered_cities.index)].to_dict()
    rounded_dict = {key: round(value,4) for key, value in get_top_cities_by_vacancies(vacancies_by_area).items()}
    print(f"Доля вакансий по городам: {rounded_dict}")

    # Доля вакансий по городам для выбранной профессии (в порядке убывания)
    data_prof = df[df['name'].str.contains(profession_name, case=False, na=False)]
    prof_vacancies_by_area = data_prof['area_name'].value_counts(normalize=True)
    prof_vacancies_by_area = prof_vacancies_by_area[
        prof_vacancies_by_area.index.isin(filtered_cities.index)].to_dict()
    rounded_dict_city = {key: round(value,4) for key, value in get_top_cities_by_vacancies(prof_vacancies_by_area).items()}
    print(f"Доля вакансий по городам для выбранной профессии: {rounded_dict_city}")

    df = df.dropna(subset=["salary"])
    data_prof = data_prof.dropna(subset=["salary"])
    # Уровень зарплат по городам (в порядке убывания)
    salaries_by_area = df.groupby('area_name')['salary'].mean().astype(int)
    salaries_by_area = salaries_by_area[
        salaries_by_area.index.isin(filtered_cities.index)].sort_values(ascending=False).to_dict()

    rounded_dict = {key: round(value) for key, value in get_top_cities_by_salary(salaries_by_area).items()}
    print(f"Уровень зарплат по городам: {get_top_cities_by_salary(salaries_by_area)}")

    # Уровень зарплат по городам для выбранной профессии (в порядке убывания)
    prof_salaries_by_area = data_prof.groupby('area_name')['salary'].mean().astype(int)
    prof_salaries_by_area = prof_salaries_by_area[
        prof_salaries_by_area.index.isin(filtered_cities.index)].sort_values(ascending=False).to_dict()

    print(f"Уровень зарплат по городам для выбранной профессии {get_top_cities_by_salary(prof_salaries_by_area)}")


def get_skills_page_content(df: pd.DataFrame):
    df["key_skills"] = df["key_skills"].apply(lambda row: [] if pd.isnull(row) else row.split("\n"))
    skills_freq = df.explode("key_skills").groupby(["published_year", "key_skills"]).size().reset_index(
        name="frequency")
    #если сикллов нету пустой массив если есть сто сплит и делаем частоту
    top_skills = (
        skills_freq.groupby("published_year")
        .apply(lambda x: x.nlargest(20, "frequency"))
        .reset_index(drop=True)
    )
    # 20  наиболее встречающихся

    skills_frequency_by_year = top_skills.groupby("published_year").apply(
        lambda x: [x["key_skills"].to_list(), x["frequency"].to_list()]).to_dict()
    # создаем словарь ключи года значения массив из 2 массивов
    print(f"ТОП-20 навыков по годам: {skills_frequency_by_year}")

def print_skills(df: pd.DataFrame):
    df["key_skills"] = df["key_skills"].apply(lambda row: [] if pd.isnull(row) else row.split("\n"))
    skills_freq = df.explode("key_skills").groupby(["published_year", "key_skills"]).size().reset_index(
        name="frequency")

    top_skills = (
        skills_freq.groupby("published_year")
        .apply(lambda x: x.nlargest(20, "frequency"))
        .reset_index(drop=True)
    )
    skills_frequency_by_year: dict = top_skills.groupby("published_year").apply(
        lambda x: [x["key_skills"].to_list(), x["frequency"].to_list()]).to_dict()

    for skill_by_year in skills_frequency_by_year.keys():
        array = skills_frequency_by_year[skill_by_year]
        dict = {x: y for x, y in zip(array[0], array[1])}
        print(f"{skill_by_year}: {json.dumps(dict, ensure_ascii=False).encode('utf-8').decode()}")


def get_top_cities_by_vacancies(cities: dict) -> dict:
    top_cities = dict(list(cities.items())[:15])
    other_cities_sum = 1 - sum(top_cities[city] for city in top_cities)
    top_cities["Другие"] = other_cities_sum
    return top_cities

# количество городов :15
def get_top_cities_by_salary(cities: dict) -> dict:
    top_cities = dict(list(cities.items())[:15])
    other_cities_sum = sum(cities[item] for item in cities if item not in top_cities) / (len(cities) - 15)
    top_cities["Другие"] = int(other_cities_sum)
    return top_cities

# def view_func():
#     return get_demand_page_content(data.copy())

# Подготовка данных из файла для аналитики. Запись обработанного файла в новый, чтобы больше не обращаться к API ЦБ
# file_name = r"D:\Загрузки\vacancies_for_web.csv"
# data = pd.read_csv(file_name)
# data = prepare_df(data)
# data.to_csv("vacancies_with_salary1.csv", index=False, encoding='utf-8')

file_name = r"vacancies_with_salary.csv"
# Вводить через regex все возможные названия через |
profession_name = r"1с разработчик|1c разработчик|1с|1c|1 c|1 с"
data = pd.read_csv(file_name)
get_demand_page_content(data.copy())
get_geography_page_content(data.copy())
get_skills_page_content(data.copy())
# Еще 1 раз вызываю эту функцию для скиллов для получения навыков для выбранной профессии
get_skills_page_content(data[data['name'].str.contains(profession_name, case=False, na=False)].copy())

print()
print_skills(data.copy())
print()
print_skills(data[data['name'].str.contains(profession_name, case=False, na=False)].copy())