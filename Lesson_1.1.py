# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
# для конкретного пользователя, сохранить JSON-вывод в файле *.json.

# документацию можно посмотреть здесь https://docs.github.com/en/rest

import requests

username = 'Usalina'
token = ''
r = requests.get('https://api.github.com/user/repos', auth=(username, token))
r.json()
f = open("requests.json", "w")
f.write(r)
f.close()

