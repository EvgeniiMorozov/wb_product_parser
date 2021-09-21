from random import randint
from time import sleep

from bs4 import BeautifulSoup
import requests
from config import HEADERS

products = []


def get_content(url):
    return requests.get(url, headers=HEADERS).text


def get_prod_ids(content):
    soup = BeautifulSoup(content, 'html.parser')
    cards = soup.find_all('div', class_='product-card j-card-item')
    products_ids = []
    for card in cards:
        product_id = card.find('a', class_='product-card__main j-open-full-product-card').get('href')
        # '/catalog/15875681/detail.aspx?targetUrl=GP'
        product_id = [el for el in product_id.split('/')]
        products_ids.append(product_id[2])

    products.extend(products_ids)


def main():
    pages = 1
    for page in range(1, pages+1):
        print(f'Страница {page} из {pages}...')
        # f'https://www.wildberries.ru/catalog/elektronika/noutbuki-pereferiya/noutbuki-ultrabuki?page=5&fbrand=6049%3B24012%3B6667%3B6364%3B19467%3B3859%3B5786'
        url = f'https://www.wildberries.ru/catalog/elektronika/smartfony-i-telefony/vse-smartfony?sort=popular&page={page}&fbrand=5789%3B6049%3B5786%3B5779%3B16111%3B10883%3B28380%3B132943%3B5772'
        content = get_content(url)
        get_prod_ids(content)
        sleep(randint(8, 12))

    with open('phones_ids.txt', 'w') as file:
        for product in products:
            file.write(product+'\n')


if __name__ == '__main__':
    main()
