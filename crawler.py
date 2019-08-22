import requests
import csv
from bs4 import BeautifulSoup
import pandas as pd

f = csv.writer(open('americanas.csv', 'w'))
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

url = 'https://ri.lasa.com.br/lojas?all'

page = requests.get(url)
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

for el in store_state:
    index = store_state.index(el)
    state = states[index]
    for value in range(el):
        name = names[value]
        city = cities[value]
        address = addresses[value]
        f.writerow(['', '', '', '', '', city, state,
                    '', 'Brasil', '', address, '', ''])
