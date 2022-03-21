# Посмотреть документацию к API GitHub,
# разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import json
from pprint import pprint


# username - achebotarenko
username = input('Enter username: ')
response = requests.get(f'https://api.github.com/users/{username}/repos')

repos_list = {f'{username} repositories': []}
with open('user_repos.json', 'w') as f:
    for repo in response.json():
        repos_list[f'{username} repositories'].append({'name': repo['name']})
    json.dump(repos_list, f)
pprint(repos_list)
