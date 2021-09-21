from random import randint
import re
import requests
import json
from pathlib import Path
from time import sleep

from bs4 import BeautifulSoup
from config import HEADERS, HTTPS_PREF, phone_spec_pattern, phone_local_path_pref

PROD_ID_LIST = ["21264155", "26301070", "17853563", "23484561"]

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

    vendor_code = soup.find("div", class_="same-part-kt__common-info").find("span", class_="hide-desktop")
    vendor_code = vendor_code.find_next("span").get_text(strip=True)

    # slider_soup
    swiper_container = slider_soup.find("ul", class_="swiper-wrapper")
    img_items = swiper_container.find_all("li")
    img_links = []
    for i in range(3):
        # <img src="//images.wbstatic.net/tm/new/26820000/26828281-1.jpg" alt=" Вид 1.">
        # '//images.wbstatic.net/c324x432/new/23480000/23484561-1.jpg'
        link = img_items[i].find("div", class_="slide__content").find("img").get("src")
        image_link = ''.join(re.sub(r"/tm/", "/big/", link))
        # filename = re.search(r'/(\d{6,8}-\d\.jpg)$', image_link)
        filename = image_link.split('/')[-1]
        image_url_link = HTTPS_PREF + image_link
        image_local_link = phone_local_path_pref + vendor_code + '/' + filename
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

    details_table = details_soup.find("div", class_="product-params")
    table_rows = details_table.find_all("tr", class_="product-params__row")

    search_list = phone_spec_pattern.keys()

    specification = {}

    for row in table_rows:
        key_row_text = row.find("span", class_="product-params__cell-decor").find("span").get_text()
        if key_row_text in search_list:
            spec_key = phone_spec_pattern[key_row_text]
            try:
                specification[spec_key] = row.find("td", class_="product-params__cell").get_text(strip=True)
            except Exception as ex:
                specification[spec_key] = None

    result = {
        "brand": brand,
        "model": specification["model"],
        "vendor": vendor_code,
        "price": price,
        "description": description_text,
        "specification": specification,
        "images_urls": img_links,
    }
    # print(result)
    make_json_file(f"{vendor_code}", result)


def make_json_file(filename, data):
    path = f"source/phones/{filename}"
    if not Path(path).exists():
        Path(path).mkdir()
    with open(path + f"/{filename}.json", "w", encoding="UTF-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    for product_id in PROD_ID_LIST:
        sleep(randint(5, 7))
        url = (
            f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx?targetUrl=GP"
        )
        html = get_html(url)
        get_content(html)

    with open('phone_images_urls.txt', 'w') as file:
        for url in images_urls:
            file.write(url + '\n')


if __name__ == '__main__':
    main()
