from collections import defaultdict
import time
from random import randint
import re
import requests
import json
from pathlib import Path

from bs4 import BeautifulSoup
from config import HEADERS, HTTPS_PREF, notebook_local_path_pref, notebook_spec_pattern

PROD_ID_LIST = ["29600233", "25925048", "26009431", "34212494", "40597292"]

# PROTO_URL = f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx?targetUrl=GP"

# Main page (Oppo, A74, 19990rub): https://images.wbstatic.net/c246x328/new/26820000/26828281-1.jpg
# Product page: slider main -      https://images.wbstatic.net/big/new/26820000/26828281-1.jpg
#               slider nav  -      https://images.wbstatic.net/tm/new/26820000/26828281-1.jpg

images_urls = []


def get_html(url):
    return requests.get(url, headers=HEADERS).text


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    header_soup = soup.find("div", class_="same-part-kt__header-wrap")
    slider_soup = soup.find("div", class_="same-part-kt__slider-wrap j-card-left-wrap")
    price_soup = soup.find("div", class_="same-part-kt__info-wrap")
    details_soup = soup.find("section", class_="product-detail__details details")

    # header_soup
    brand = (
        header_soup.find("h1", class_="same-part-kt__header").find_next("span").get_text(strip=True))
    print(brand)
    vendor_code = soup.find("div", class_="same-part-kt__common-info").find("span", class_="hide-desktop")
    vendor_code = vendor_code.find_next("span").get_text(strip=True)

    # slider_soup
    swiper_container = slider_soup.find("ul", class_="swiper-wrapper")
    img_links = []
    img_items = swiper_container.find_all("img")

    for i in range(min(len(img_items), 3)):
        # <img src="//images.wbstatic.net/tm/new/26820000/26828281-1.jpg" alt=" Вид 1.">
        # '//images.wbstatic.net/c324x432/new/23480000/23484561-1.jpg'
        link = img_items[i].get("src")
        image_link = ''.join(re.sub(r"/tm/", "/big/", link))
        filename = image_link.split('/')[-1]
        image_url_link = HTTPS_PREF + image_link
        image_local_link = notebook_local_path_pref + vendor_code + '/' + filename
        img_links.append(image_local_link)
        images_urls.append(image_url_link)

    # price_soup
    if not price_soup.find("span", class_="price-block__final-price"):
        price = None
    else:
        price = price_soup.find("span", class_="price-block__final-price").get_text(strip=True)
        price = price.strip('₽')
        price = int(''.join(el.strip() for el in price))

    # details_soup
    description_text = details_soup.find("p", class_="collapsable__text").get_text(strip=True)
    description_text = ' '.join(chunk.strip() for chunk in description_text.split())
    short_description = header_soup.find("h1", class_="same-part-kt__header").find_next("span")\
        .find_next('span').get_text(strip=True)

    # Определяем модель ноутбука (примерно)
    # 'Ноутбук Asus Zenbook Pro 15 OLED UX535LI Intel Core i7 10870H•RAM 16 Гб•SSD 512 Гб•Windows 10 Home'
    # model_proto = short_description.split()
    # stop_list = [brand.lower(), 'ноутбук']
    # model_proto = [el for el in model_proto if el.lower() not in stop_list]
    # model = ' '.join(model_proto[:2])

    details_table = details_soup.find("div", class_="product-params")
    table_rows = details_table.find_all("tr", class_="product-params__row")

    search_list = notebook_spec_pattern.keys()

    specification = defaultdict()
    specification.default_factory = lambda: 'Уточнить'
    # specification['model'] = model

    for row in table_rows:
        key_row_text = row.find("span", class_="product-params__cell-decor").find("span").get_text()
        if key_row_text in search_list:
            try:
                spec_key = notebook_spec_pattern[key_row_text]
                specification[spec_key] = row.find("td", class_="product-params__cell").get_text(strip=True)
            except Exception as ex:
                spec_key = notebook_spec_pattern[key_row_text]
                specification[spec_key] = None

    result = {
        "brand": brand,
        # "model": specification['model'],
        "vendor": vendor_code,
        "short_description": short_description,
        "price": price,
        "description": description_text,
        "specification": specification,
        "images_urls": img_links,
    }

    # print(result)
    make_json_file(f"{vendor_code}", result)


def make_json_file(filename, data):
    path = f"source/notebooks/{filename}"
    if not Path(path).exists():
        Path(path).mkdir()
    with open(path + f"/{filename}.json", "w", encoding="UTF-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    start = time.time()

    with open('notebooks_ids.txt', 'r') as file:
        product_ids = file.readlines()
    product_ids = [chunk.strip() for chunk in product_ids]
    # product_ids = PROD_ID_LIST

    for idx, product_id in enumerate(product_ids, start=1):
        time.sleep(randint(5, 7))
        print(f'{idx} - {product_id}')
        url = (
            f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx?targetUrl=GP"
        )
        html = get_html(url)
        get_content(html)

    with open('notebook_images_urls.txt', 'w') as file:
        for url in images_urls:
            file.write(url + '\n')

    end = time.time()
    print(end-start)


if __name__ == '__main__':
    main()
