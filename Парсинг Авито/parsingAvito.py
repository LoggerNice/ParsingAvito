from bs4 import BeautifulSoup
import requests
import csv


URL  = 'https://www.avito.ru/balakovo/avtomobili/chevrolet/lacetti/sedan-ASgBAQICAkTgtg32lyjitg3oqCgBQOa2DRTKtyg?cd=1&radius=400'
HEADERS = { 'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 OPR/78.0.4093.184 (Edition Yx)'}
FILE = 'cars.csv'


def get_html(url, params = None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagnav = soup.find_all('span', class_ = 'pagination-item-JJq_j')

    if pagnav:
        return pagnav[len(pagnav) - 2].get_text()
    else:
        return 1


def get_cont(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_ = 'iva-item-root-Nj_hb')

    cars = []
    for item in items:
        cars.append({
            'title': item.find('h3', class_ = 'title-root-j7cja').get_text(),
            'link': 'https://www.avito.ru' + item.find('a', class_ = 'link-link-MbQDP').get('href'),
            'city': item.find('div', class_ = 'geo-georeferences-Yd_m5').get_text(),
            'price': item.find('span', class_ = 'price-price-BQkOZ').get_text(),
            'date': item.find('div', class_ = 'date-text-VwmJG').get_text()
        })  
    return cars

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter = ';')
        writer.writerow(['Название', 'Ссылка', 'Город', 'Дата выхода'])

        print(items)

        for item in items:
            writer.writerow([item['title'], item['link'], item['city'], item['date']])


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        cars = []       
        pages = int(get_pages_count(html.text))

        for page in range(1, pages + 1):
            print(f'Парсинг {page}...')
            html = get_html(URL, params={'p': page})
            cars.extend(get_cont(html.text))

        save_file(cars, FILE)
    else:
        print('Ошибка')

parse()