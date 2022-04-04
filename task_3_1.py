import pymongo
from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
import re

client = MongoClient('localhost', 27017)
db = client['hh_vacancy']
vacancy = db['search_list']
main_url = 'https://hh.ru/search/vacancy'
search_position = input('Введите должность для поиска: ')
while 1:
    try:
        page = int(input('Введите количество страниц для поиска: '))
        break
    except ValueError:
        print('Введите целое число')

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36'}

params = {'text': search_position, 'page': 0}

list_of_position = []


def insert_vacancy(vac):
    try:
        vacancy.insert_one(vac)
    except pymongo.errors.DuplicateKeyError:
        pass


def search_vacancy(salary):
    for item in vacancy.find({"$or": [{'salary_min': {"$gt": salary}}, {'salary_max': {"$gt": salary}}]}):
        print(item)


while params['page'] < page:
    response = requests.get(main_url, params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    positions = dom.find_all('div', {'class': "vacancy-serp-item"})

    if response.ok and positions:
        for position in positions:
            pos_list = {}
            link = position.find('a', {'data-qa': "vacancy-serp__vacancy-title"}).get('href')
            id = re.search(r'\d+', link).group()
            name = position.find('a', {'data-qa': "vacancy-serp__vacancy-title"}).text
            try:
                salary = position.find('span', {'data-qa': "vacancy-serp__vacancy-compensation"}).text.split(' ')
                if len(salary) == 4:
                    salary_min = int(salary[0].replace('\u202f', ''))
                    salary_max = int(salary[2].replace('\u202f', ''))
                    salary_currency = salary[3].replace('\xa0', '')
                elif salary[0] == 'от':
                    salary_min = int(salary[1].replace('\u202f', ''))
                    salary_max = None
                    salary_currency = salary[2].replace('\xa0', '')
                elif salary[0] == 'до':
                    salary_min = None
                    salary_max = int(salary[1].replace('\u202f', ''))
                    salary_currency = salary[2].replace('\xa0', '')
            except:
                salary_min = None
                salary_max = None
                salary_currency = None

            pos_list['id'] = id
            pos_list['name'] = name
            pos_list['link'] = link
            pos_list['salary_min'] = salary_min
            pos_list['salary_max'] = salary_max
            pos_list['salary_currency'] = salary_currency
            insert_vacancy(pos_list)
            list_of_position.append(pos_list)
    params['page'] += 1

for vac_list in vacancy.find():
    print(vac_list)

salary = int(input('Вакансии с зарплатой от: '))
search_vacancy(salary)
