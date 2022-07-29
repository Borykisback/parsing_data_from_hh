import requests, json, time, os, pyodbc, shutil

server = 'SMSERVER\OLAPSERVER' 
database = 'database' 
username = 'username' 
password = 'password' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

filee = 'Documents/parsing_HHAPI/data'
user = os.getlogin()
print(user)
try:
    os.makedirs(filee)
    print("Путь создан")
except:
    next
    #shutil.rmtree(filee)
    #print("Путь пересоздан")

def getPage(page = 0):
     
    params = {
        'area': 1,
        'page': page,
        'per_page': 100
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

    print("страница:" + str(page))
    time.sleep(0.25)
    xlrange = page

print('Старницы поиска собраны')

x = 0
row = 2 
while x <= xlrange:
    with open(f"Documents/parsing_HHAPI/data/{x}.json", "r", encoding='utf8') as json_file:
        a = json.load(json_file)
    
    for items in a:
        count = cursor.execute(f"INSERT INTO Industry (id_ind_name, name) VALUES ('{items['id']}', '{items['name']}');").rowcount
        cnxn.commit()
        for ind_items in items['industries']:
            count = cursor.execute(f"INSERT INTO Industry (id_ind_name, name) VALUES ('{ind_items['id']}', '{ind_items['name']}');").rowcount
            cnxn.commit()
    print('Rows inserted: ' + str(count))

    x += 1