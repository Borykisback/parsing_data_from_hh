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
     
     
    req = requests.get('https://api.hh.ru/industries', params) 
    data = req.content.decode() 
    req.close()
    return data

xlrange = 0
for page in range(0, 1):

    jsObj = json.loads(getPage(page))
    nextFileName = 'Documents/parsing_HHAPI/data/{}.json'.format(len(os.listdir('Documents/parsing_HHAPI/data/')))

    f = open(nextFileName, mode='w', encoding='utf8')
    f.write(json.dumps(jsObj, ensure_ascii=False))
    f.close()
    
    #if (jsObj['pages'] - page) <= 1:
    #    break
    
    print("страница:" + str(page))
    time.sleep(0.25)
    xlrange = page

print('Старницы поиска собраны')

book=openpyxl.Workbook()
page = book.active
x = 0
row = 2 
while x <= xlrange:
    with open(f"Documents/parsing_HHAPI/data/{x}.json", "r", encoding='utf8') as json_file:
        a = json.load(json_file)

    page['A1'] = 'ID'
    page['B1'] = 'NAME'
    
    for items in a:
        page[row][0].value = items['id']
        page[row][1].value = items['name']
        row += 1
        for ind_items in items['industries']:
            page[row][0].value = ind_items['id']
            page[row][1].value = ind_items['name']
            row += 1



    x += 1
book.save("Documents/parsing_HHAPI/HH_API.xlsx")
print("Данные записаны")
print(f"путь к файлам: 'Users/{user}/Documents/parsing_HHAPI'")
book.close()