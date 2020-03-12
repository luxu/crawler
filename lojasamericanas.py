from requests import get
from bs4 import BeautifulSoup
import csv
from time import sleep
from tqdm import tqdm

url = 'https://ri.lasa.com.br/lojas?all'

page = get(url)
soup = BeautifulSoup(page.text, 'html.parser')

store_list = soup.find_all(class_='lojas')[2]

store_list_state_items = store_list.find_all('h3')
fields_store_items = store_list.find_all('ul')

# Values
states = []
names = []
store_state = []
cities = []
addresses = []


for state in store_list_state_items:
    state_name = state.contents[1]
    states.append(state_name)

for field in fields_store_items:
    store_name_items = field.contents[3].find_all(class_='name')
    store_state.append(len(store_name_items))
    store_city_items = field.contents[3].find_all(class_='cidade')
    values_store_items = field.contents[3].find_all(class_='col-md-10')
    for name in store_name_items:
        store_name = name.text
        names.append(store_name)
    for city in store_city_items:
        store_city = city.text
        cities.append(store_city)
    for value in values_store_items:
        address = value.contents[3].text
        addresses.append(address)


class CSV(object):
    def __init__(self,path,mode):
        self.path = path
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.path,self.mode)
        if self.mode == 'r':
            return csv.reader(self.file)
        elif self.mode == 'w':
            return csv.writer(self.file)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

with CSV('americanas.csv', 'w') as f:
    f.writerow(['Logradouro',
                'Endereço',
                'Numero',
                'Complemento',
                'Bairro',
                'Cidade',
                'Estado',
                'Região',
                'País',
                'CEP',
                'Endereço completo',
                'Latitude',
                'Longitude'])
    for el in store_state:
        index = store_state.index(el)
        state = states[index]
        contador = tqdm(range(el))
        print(f'{state}\n{"*"*80}')
        for value in contador:
            contador.set_description(f"Processing {value}")
            name = names[value]
            city = cities[value]
            address = addresses[value]
            f.writerow(['', '', '', '', '', city, state, '', 'Brasil', '', address, '', ''])
            if 'Joaquim' in address:
                print(f'Name.: {name} - City.: {city}')
            sleep(0.25)
        print(f'{"*"*30} FIM DO {state} {"*"*30}\n')
print('Fim do arquivo... :-)')