from bs4 import BeautifulSoup

FILE = "source/page_content/page_1.txt"
HOST = "https://www.wildberries.ru"
HOST_PREF = "https:"

img_links = []
prod_links = []


def load_content(filename):
    with open(filename, "r", encoding="UTF-8") as file:
        data = file.readlines()
    print(type(data))
    # print(data)

    return "".join(data)


def encoding_data(data):
    soup = BeautifulSoup(data, "lxml")
    items = soup.find_all("div", class_="product-card__wrapper")
    data = []
    for item in items:
        prod_link = HOST + item.find("a", class_="product-card__main j-open-full-product-card").get("href")
        img_link = item.find("img", class_="j-thumbnail thumbnail").get("data-original")
        print(type(img_link))
        # img_link = HOST_PREF + str(img_link)
        # img_links.extend(img_link)
        description = item.find("a", class_="product-card__main j-open-full-product-card").get("alt")
        prod_links.extend(prod_link)
        brand_div = item.find("div", class_="product-card__brand-name")
        brand = brand_div.find("strong", class_="brand-name").get_text()
        spec_proto = brand_div.find("span", class_="goods-name").get_text()
        print(img_link)
        print(prod_link)

        data.extend({
            "brand": brand,
            "product_url": prod_link,
            "img_url": img_link,
            "description": description
        })


def main():
    data = load_content(FILE)
    encoding_data(data)


if __name__ == '__main__':
    main()
