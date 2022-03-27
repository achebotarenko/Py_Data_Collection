from bs4 import BeautifulSoup
import requests
from pprint import pprint

main_url = 'https://hh.ru/search/vacancy'
search_position = input('Введите должность для поиска: ')
while 1:
        try:
            page = int(input('Введите количество страниц для поиска: '))
            break
        except ValueError:
            print('Введите целое число')

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36'}
list_of_position = []


def parse_page(p):
    params = {'text': search_position, 'page': p}
    response = requests.get(main_url, params=params, headers=headers)
    if response.ok:
        dom = BeautifulSoup(response.text, 'html.parser')
        positions = dom.find_all('div', {'class': "vacancy-serp-item"})
        for position in positions:
            link = position.find('a', {'data-qa': "vacancy-serp__vacancy-title"}).get('href')
            name = position.find('a', {'data-qa': "vacancy-serp__vacancy-title"}).text
            salary_dict = {}
            try:
                salary = position.find('span', {'data-qa': "vacancy-serp__vacancy-compensation"}).text.split(' ')
                if len(salary) == 4:
                    salary_dict = dict((('мин',  int(salary[0].replace('\u202f', ''))), ('макс', int(salary[2].replace('\u202f', ''))), (('валюта'), salary[3].replace('\xa0',  ''))))
                elif len(salary) == 3 and salary[0] == 'от':
                    salary_dict = dict((('мин', int(salary[1].replace('\u202f', ''))), (('валюта'), salary[2].replace('\xa0', ''))))
                elif len(salary) == 3 and salary[0] == 'до':
                    salary_dict = dict((('макс', int(salary[1].replace('\u202f', ''))), (('валюта'), salary[2].replace('\xa0', ''))))
            except:
                salary_dict = {'З/П не указана'}
            list_of_position.append((link, name, salary_dict))


for i in range(page):
    parse_page(i)
pprint(list_of_position)
