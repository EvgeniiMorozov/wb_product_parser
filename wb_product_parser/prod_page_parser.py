# import asyncio
from random import randint
import re
import requests
import json
from pathlib import Path
from time import sleep

# from aiohttp import ClientSession
from bs4 import BeautifulSoup

HEADERS = {
    "user agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like"
        " Gecko) Chrome/92.0.4515.131 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
}
HOST = "https://www.wildberries.ru"
HOST_PREF = "https:"
PROD_ID_LIST = ["21264155", "26301070"]

# PROTO_URL = f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx?targetUrl=GP"

# Main page (Oppo, A74, 19990rub): https://images.wbstatic.net/c246x328/new/26820000/26828281-1.jpg
# Product page: slider main -      https://images.wbstatic.net/big/new/26820000/26828281-1.jpg
#               slider nav  -      https://images.wbstatic.net/tm/new/26820000/26828281-1.jpg

fetching_data = []


def get_html(url, params=None):
    print(f"{url=}")
    return requests.get(url, headers=HEADERS, params=None).text


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
        link = img_items[i].find("div", class_="slide__content").find("img").get("src")
        image_link = re.sub(r"/tm/", "/big/", link)
        img_links.append("".join(image_link))

    # price_soup
    if not price_soup.find("span", class_="price-block__final-price"):
        price = "-"
    else:
        price = price_soup.find("span", class_="price-block__final-price").get_text(strip=True)

    # details_soup
    description_text = details_soup.find("p", class_="collapsable__text").get_text(strip=True)
    details_table = details_soup.find("div", class_="product-params")
    table_rows = details_table.find_all("tr", class_="product-params__row")
    specification_dict = {}
    for row in table_rows:
        if row.find("th", class_="product-params__cell").find("span", class_="product-params__cell-decor").find("span").get_text() == "Операционная система":
            specification_dict["operating_system"] = row.find("td", class_="product-params__cell").get_text(strip=True)

        elif row.find("th", class_="product-params__cell").find("span", class_="product-params__cell-decor").find("span").get_text() == "Модель":
            specification_dict["model"] = row.find("td", class_="product-params__cell").get_text(strip=True)

        elif row.find("th", class_="product-params__cell").find("span", class_="product-params__cell-decor").find("span").get_text() == "Гарантийный срок":
            specification_dict["guarantee"] = row.find("td", class_="product-params__cell").get_text(strip=True)

        elif row.find("th", class_="product-params__cell").find("span", class_="product-params__cell-decor").find("span").get_text() == "Тип дисплея/экрана":
            specification_dict["display_type"] = row.find("td", class_="product-params__cell").get_text(strip=True)

        elif row.find("th", class_="product-params__cell").find("span", class_="product-params__cell-decor").find("span").get_text() == "Диагональ экрана":
            specification_dict["screen_diagonal"] = row.find("td", class_="product-params__cell").get_text(strip=True)

        elif row.find("th", class_="product-params__cell").find("span", class_="product-params__cell-decor").find("span").get_text() == "Разрешение экрана":
            specification_dict["screen_resolution"] = row.find("td", class_="product-params__cell").get_text(strip=True)

        elif row.find("th", class_="product-params__cell").find("span", class_="product-params__cell-decor").find("span").get_text() == "Процессор":
            specification_dict["cpu"] = row.find("td", class_="product-params__cell").get_text(strip=True)

        elif row.find("th", class_="product-params__cell").find("span", class_="product-params__cell-decor").find("span").get_text() == "Объем встроенной памяти (Гб)":
            specification_dict["ROM_size"] = row.find("td", class_="product-params__cell").get_text(strip=True)

        elif row.find("th", class_="product-params__cell").find("span", class_="product-params__cell-decor").find("span").get_text() == "Объем оперативной памяти (Гб)":
            specification_dict["RAM_size"] = row.find("td", class_="product-params__cell").get_text(strip=True)

        elif row.find("th", class_="product-params__cell").find("span", class_="product-params__cell-decor").find("span").get_text() == "Емкость аккумулятора":
            specification_dict["battery_capacity"] = row.find("td", class_="product-params__cell").get_text(strip=True)

        elif row.find("th", class_="product-params__cell").find("span", class_="product-params__cell-decor").find("span").get_text() == "Количество мп основной камеры":
            specification_dict["main_camera_resolution"] = row.find("td", class_="product-params__cell").get_text(strip=True)

    result = {
        "brand": brand,
        "model": specification_dict["model"],
        "vendor": vendor_code,
        "price": price,
        "description": description_text,
        "specification": specification_dict,
        "images_urls": img_links,
    }
    print(result)
    make_json_file(f"{vendor_code}", result)


def make_json_file(filename, data):
    path = f"source/json/{filename}"
    if not Path(path).exists():
        Path(path).mkdir()
    with open(path + f"/{filename}.json", "w", encoding="UTF-8") as file:
        file.write(json.dumps(data))


def main():
    for product_id in PROD_ID_LIST:
        sleep(randint(8, 12))
        url = (
            f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx?targetUrl=GP"
        )
        html = get_html(url)
        get_content(html)


if __name__ == '__main__':
    main()
