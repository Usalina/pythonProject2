# Необходимо собрать информацию о вакансиях на вводимую должность
# (используем input или через аргументы получаем должность) с сайтов HH(обязательно)
# и/или Superjob(по желанию). Приложение должно анализировать несколько страниц сайта
# (также вводим через input или аргументы).

# Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.
# Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv.

import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import re
import random

url = 'http://127.0.0.1:5000/'

headers = {'User-agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36'}
def hh(main_link, search_str, n_str):
    #n_str - кол-во просматриваемых страниц
    html = requests.get(main_link+'/search/vacancy?clusters=true&enable_snippets=true&text='+search_str+'&showClusters=true', headers=headers).text
    parsed_html = bs(html,'lxml')

    jobs = []
    for i in range(n_str):
        jobs_block = parsed_html.find('div',{'class':'vacancy-serp'})
        jobs_list = jobs_block.findChildren(recursive=False)
        for job in jobs_list:
            job_data={}
            req=job.find('span',{'class':'g-user-content'})
            if req!=None:
                main_info = req.findChild()
                job_name = main_info.getText()
                job_link = main_info['href']
                salary = job.find('div',{'class':'vacancy-serp-item__sidebar'})
                salary1 = salary.getText()
                salary2 = salary.getText().replace(u'\xa0', u'')
                salaries = salary1.split(' ')
                salaries1 = salary2.split(' ')
                if not salary:
                    salary_min=None
                    salary_max=None
                    salary_currency = None
                else:
                    if str(salaries[0]) == "от":
                        #salary = salary.getText().replace(u'\xa0', u'')
                        #salaries1 = salary.split(' ')
                        salaries1[0] = re.sub(r'[^0-9]', '', salaries1[0])
                        salary_min = salaries1[1]
                        salary_max = None
                        salary_currency = salaries[-1]
                    elif str(salaries[0]) == 'до':
                        #salary = salary.getText().replace(u'\xa0', u'')
                        #salaries1 = salary.split(' ')
                        salaries1[0] = re.sub(r'[^0-9]', '', salaries1[0])
                        salary_min = None
                        salary_max = salaries1[0]
                        salary_currency = salaries[-1]
                    else:
                        #salary=salary.getText().replace(u'\xa0', u'')
                        #salaries=salary.split(' ')
                        salaries1[0] = re.sub(r'[^0-9]', '', salaries1[0])
                        salary_min=salaries1[0]
                        salaries1[1] = re.sub(r'[^0-9]', '', salaries1[1])
                        salary_max = salaries1[1]
                        salary_currency = salaries[-1]


                job_data['name'] = job_name
                job_data['salary_currency'] = salary_currency
                job_data['salary_min'] = salary_min
                job_data['salary_max'] = salary_max
                job_data['link'] = job_link
                job_data['site'] = main_link
                jobs.append(job_data)
        #time.sleep(random.randint(1,10))
        #next_btn_block=parsed_html.find('a',{'class':'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
        #next_btn_link=next_btn_block['href']
        #html = requests.get(main_link+next_btn_link,headers=headers).text
        #parsed_html = bs(html,'lxml')

    pprint(jobs)
    return jobs

search_str='Python'
n_str=2

hh('https://yakutsk.hh.ru',search_str,n_str)
