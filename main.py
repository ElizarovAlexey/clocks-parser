import os
import time
import requests
from bs4 import BeautifulSoup

import db_connection

domain = 'https://golden-time.ru'


def get_all_pages():
    url = 'https://golden-time.ru/catalog/wristwatch/filter/country-rossiya/'

    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

    response = requests.get(url=url, headers=headers)

    if not os.path.exists('data'):
        os.mkdir('data')

    with open('data/golden-time.html', 'w', encoding="utf-8") as file:
        file.write(response.text)

    with open('data/golden-time.html', encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    pages_count = int(soup.find('div', class_='modern-page-navigation').find_all('a')[-2].text)

    for i in range(1, pages_count + 1):
        url = domain + f'/catalog/wristwatch/filter/country-rossiya/?PAGEN_1={i}'

        response = requests.get(url=url, headers=headers)

        with open(f'data/golden-time-{i}.html', 'w', encoding="utf-8") as file:
            file.write(response.text)

        time.sleep(2)

    return pages_count


def collect_data(pages_count):
    products = []
    for page in range(1, pages_count + 1):
        with open(f'data/golden-time-{page}.html', 'r', encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        items_card = soup.find_all('div', class_='product-item')

        for item in items_card:
            product_collection = item.find('div', class_='product-item__collection').text.strip()
            product_name = item.find('div', class_='product-item__name').text.strip()
            product_type = item.find('div', class_='product-item__name-prefix').text.strip()
            product_price = item.find('div', class_='product-item__price').text.strip()[:-2]
            product_link = domain + item.find('a', class_='product-item__img').get('href').strip()

            product = {
                'Collection': product_collection,
                'Name': product_name,
                'Type': product_type,
                'Price': product_price,
                'Link': product_link
            }

            products.append(product)

    return products


def save_products(products):
    db_connection.collection.insert_many(products)


def main():
    # pages_count = get_all_pages()
    products = collect_data(1)
    save_products(products)


if __name__ == '__main__':
    main()
