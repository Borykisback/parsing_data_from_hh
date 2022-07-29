import requests
import json
import time
import os
import openpyxl

user = os.getlogin()
print(user)
try:
    os.makedirs('Documents/parsing_HHAPI/data')
    print("Путь создан")
except:
    print("Папки существуют (TRUE)")

def getPage(page = 0):
    """
    Создаем метод для получения страницы со списком вакансий.
    Аргументы:
        page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
    """
     
    params = {
        #'text': 'NAME:продавец', # Текст фильтра
        'area': 1, # Поиск ощуществляется по вакансиям города Москва
        'page': page, # Индекс страницы поиска на HH
        'per_page': 100 # Кол-во вакансий на 1 странице
    }
     
     
    req = requests.get('https://api.hh.ru/vacancies', params) 
    data = req.content.decode() 
    req.close()
    return data

for page in range(0, 5):

    jsObj = json.loads(getPage(page))
    nextFileName = 'Documents/parsing_HHAPI/data/{}.json'.format(len(os.listdir('Documents/parsing_HHAPI/data/')))

    f = open(nextFileName, mode='w', encoding='utf8')
    f.write(json.dumps(jsObj, ensure_ascii=False))
    f.close()
    
    if (jsObj['pages'] - page) <= 1:
        break
    
    print("страница:" + str(page))
    time.sleep(0.25)

print('Старницы поиска собраны')

listdirjson = 0
for filename in os.listdir(path ='Documents\parsing_HHAPI\data'):
    listdirjson += 1
listdirjson -= 1
book=openpyxl.Workbook()
page = book.active
x = 0
row = 2 
while x <= listdirjson:
    with open(f"Documents/parsing_HHAPI/data/{x}.json", "r", encoding='utf8') as json_file:
        a = json.load(json_file)

    page['A1'] = 'ID'
    page['B1'] = 'NAME'
    page['C1'] = 'CITY'
    
    
    for items in a['items']:
        try:
            page[row][0].value = items['id']
            page[row][1].value = items['name']
            page[row][2].value = items['address']['city']
        except:
            pass
        row += 1

    x += 1
book.save("Documents/parsing_HHAPI/HH_API.xlsx")
print("Данные записаны")
print(f"путь к файлам: 'Users/{user}/Documents/parsing_HHAPI'")
book.close()