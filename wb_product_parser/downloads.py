from pathlib import Path
from random import randint
from time import sleep

from config import HEADERS, phone_local_path_pref, notebook_local_path_pref
import requests


def get_content(url):
    return requests.get(url, headers=HEADERS).content


def read_file(filename):
    with open(filename, 'r', encoding='UTF-8') as file:
        data = file.readlines()
    # print(data)
    return [chunk.strip() for chunk in data]


def save_image(filename, binary_content):
    with open(filename, 'wb') as file:
        file.write(binary_content)


def main():
    urls_list = read_file('notebook_images_urls.txt')
    # urls_list = read_file('phone_images_urls.txt')
    # print(urls_list)
    # 'https://images.wbstatic.net/big/new/21260000/21264155-1.jpg'
    for idx, url in enumerate(urls_list):
        sleep(randint(5, 8))
        print(idx)
        print(url)
        filename = url.split('/')[-1]
        directory = filename.split('-')[0]
        path = notebook_local_path_pref + f'{directory}'
        # path = phone_local_path_pref + f'{directory}'
        if not Path(path).exists():
            Path(path).mkdir()
        content = get_content(url)
        save_image(path + f'/{filename}', content)


if __name__ == '__main__':
    main()
