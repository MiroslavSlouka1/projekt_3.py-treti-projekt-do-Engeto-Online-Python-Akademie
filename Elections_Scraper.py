"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Miroslav Slouka
email: miroslav.slouka@kitron.com
discord: mirek_63517
"""

import re
import requests
import csv
import sys
from bs4 import BeautifulSoup

precinct_data = {}
party_data = {}
data_of_all_parties = {}
party_names = {}
index_district = 0
stars = 0

def input_arguments():
    if len(sys.argv) != 3:
        print('Nebyly vlozeny dva argumenty')
        sys.exit(1)

    if 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=' not in sys.argv[1]:
        print('Byl vložen nesprávný parametr')
        sys.exit(1)

    return  sys.argv[1],sys.argv[2]

def data_loading(url):
    global index_district
    global stars
    index_district += 1
    server_response = requests.get(url)
    html_doc = server_response.text
    match = re.search('obec=(\\d+)', url)
    if match:
        precinct_number = match.group(1)

    soup = BeautifulSoup(html_doc, 'html.parser')
    h3_tags = soup.find_all('h3')
    for tag in h3_tags:
        text = tag.text.strip()
        if 'Obec:' in text:
            obec = text.replace('Obec: ', '')
            stars += 1
            if stars == 21:
                stars = 0
                x = '\n'
            else:
                x = '\r'
            print(x + '*' * stars, end="", flush=True)
            #print(obec)

    numbers_and_names = soup.find_all('td', {'class': ['cislo', 'overflow_name', 'sa2', 'sa3']})

    registered = ""
    envelopes = ""
    valid = ""

    for element in numbers_and_names:
        if 'sa2' in element['headers']:
            registered = element.text.replace('\xa0', '')

        if 'sa3' in element['headers']:
            envelopes = element.text.replace('\xa0', '')

        if 'sa6' in element['headers']:
            valid = element.text.replace('\xa0', '')

        if 't1sa1' in element['headers'] or 't2sa1' in element['headers']:
            if 't1sb1' in element['headers'] or 't2sb1' in element['headers']:
                party_number = int(element.text)

            if 't1sb2' in element['headers'] or 't2sb2' in element['headers']:
                party_name = element.text
                if party_number not in party_names:
                    party_names[party_number] = party_name

        if ('t1sa2' in element['headers'] and 't1sb3' in element['headers'] or
                't2sa2' in element['headers'] and 't2sb3' in element['headers']):
            valid_votes = int(element.text)
            party_data[party_number] = valid_votes

    data_of_all_parties[index_district] = list(party_data.items())
    precinct_data[index_district] = {'code': precinct_number, 'location': obec, 'registered': registered,
                                 'envelopes': envelopes, 'valid': valid}

def open_web(url):
    server_response = requests.get(url)
    html_doc = server_response.text
    soup = BeautifulSoup(html_doc, 'html.parser')

    headers = ['t1sa2', 't2sa2', 't3sa2', 's1']
    td_elements = soup.find_all('td', {'class': ['center', 'cislo'], 'headers': headers})
    for element in td_elements:
        a_elements = element.find_all('a')
        for a in a_elements:
            link = a.get('href')
            words = url.split('/')
            new_url = '/'.join(words[:-1]) + '/' + link
            if 'xvyber' not in new_url:
                open_web(new_url)
            else:
                party_data.clear()
                data_loading(new_url)

def generated_csv(csv_file):
    old_precinct = ""
    for i in precinct_data:
        new_precinct = (precinct_data[i]['code'])
        if old_precinct == new_precinct:
            dict1 = dict(data_of_all_parties[i - 1])
            dict2 = dict(data_of_all_parties[i])
            vysledek = {k: dict1.get(k, 0) + dict2.get(k, 0) for k in set(dict1) | set(dict2)}
            data_of_all_parties[i] = list(vysledek.items())
            precinct_data[i]['registered'] = str(
                    int(precinct_data[i]['registered']) + int(precinct_data[i - 1]['registered']))
            precinct_data[i]['envelopes'] = str(
                    int(precinct_data[i]['envelopes']) + int(precinct_data[i - 1]['envelopes']))
            precinct_data[i]['valid'] = str(int(precinct_data[i]['valid']) + int(precinct_data[i - 1]['valid']))

            if i - 1 in data_of_all_parties:
                data_of_all_parties.pop(i - 1)

        old_precinct = new_precinct

    fieldnames = []
    for key in precinct_data[1].keys():
        fieldnames.append(key)

    for i in range(1, max(party_names) + 1):
        if i in party_names:
            fieldnames.append(party_names[i])

    with open(csv_file, mode='w', newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(fieldnames)

        for i in data_of_all_parties:
            party_data = dict(data_of_all_parties[i])
            csv_string = []

            for key, value in precinct_data[i].items():
                csv_string.append(value)

            for j in range(1, max(party_names) + 1):
                if j in party_names:
                    csv_string.append(party_data[j])

            #print(csv_string)
            writer.writerow(csv_string)


if __name__ == '__main__':
    path,name_CSV = input_arguments()
    print('Stahuji data z vybraneho URL:',path)
    open_web(path)
    print('\n'+'Ukladam data do souboru: ',name_CSV)
    generated_csv(name_CSV)
    print('Ukoncuji program Election_Scraper ')