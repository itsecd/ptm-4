import os
import sys
import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


URL = "https://yandex.ru/images/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                         " Chrome/107.0.0.0 Safari/537.36"}


# настройка логирования
file_logger = logging.getLogger("file")
file_logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(f"lab4.log", mode='w')
file_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
file_handler.setFormatter(file_formatter)
file_logger.addHandler(file_handler)

console_logger = logging.getLogger("console")
console_logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("[%(asctime)s] %(message)s")
console_handler.setFormatter(console_formatter)
console_logger.addHandler(console_handler)


def is_valid(url: str) -> bool:
    """
    Функция, проверяющая наличие ссылки на файл в указанном атрибуте (источника)

    :param url: ссылка на изображение
    """
    if not url:
        file_logger.debug(f"No file on the: {url}")
        return False
    else:
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)


def get_images_urls(url: str, keyword: str, headers: dict, count=1000) -> list:
    """
    Функция собирает список url ведущих к файлам изображений со страницы с поисковым запросом

    :param url: ссылка на сайт с изображениями
    :param keyword: ключевое слово для поиска
    :param headers: системная информация передаваемая серверу
    :param count: количество изображений, которые необходимо скачать
    """
    page = 1
    url_list = []
    while True:
        url_page = f"{url}search?p={page}&text={keyword}"
        html_page = requests.get(url_page, headers=headers)
        soup = BeautifulSoup(html_page.content, "html.parser")
        for img in soup.find_all("img"):
            img_url = img.attrs.get("src")
            if is_valid(img_url):
                img_url = urljoin(url_page, img_url)
                if is_valid(img_url):
                    url_list.append(img_url)
            else:
                continue
        page += 1
        if len(url_list) > count:
            break
    return url_list


def download_one_image(url: str, path: str, num: int) -> None:
    """
    Функция скачивает и сохраняет одно изображение

    :param url: ссылка на изображение
    :param path: путь к папке, куда загружаются изображения 
    :param num: номер изображения
    """
    path = os.path.join("dataset", path)
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except PermissionError as ex:
            console_logger.error(f"Exception happened: {ex}", exc_info=True)
            file_logger.error(f"Exception happened: {ex}", exc_info=True)
            sys.exit()
    img = requests.get(url)
    file = os.path.join(path, f"{str(num).zfill(4)}.jpg")
    with open(file, "wb") as save:
        save.write(img.content)


def accounting_for_downloads(url: str, keyword: str, headers: dict) -> int:
    """
    Функция загружает и подсчитывает количество загруженных изображений по указанному поискового запроса

    :param url: ссылка на изображение
    :param keyword: ключевое слово для поиска
    :param headers: системная информация передаваемая серверу
    """
    imgs = get_images_urls(url, keyword, headers)
    num = 0
    for img in imgs:
        download_one_image(img, keyword, num)
        file_logger.debug(f"Image #{num} added to {keyword}")
        num += 1
    return num


def image_download(url: str, keywords: list, headers: dict) -> None:
    """
    Функция вызывающая остальные функции и оповещающая о том, по какому запросу произодится парсинг
    и сколько изображений было скачано по итогу

    :param url: ссылка на сайт с изображениями
    :param keywords: список ключевых слов
    :param headers: системная информация передаваемая серверу
    """
    if not os.path.isdir("dataset"):
        try:
            os.mkdir("dataset")
        except PermissionError as ex:
            console_logger.error(f"Exception happened: {ex}", exc_info=True)
            file_logger.error(f"Exception happened: {ex}", exc_info=True)
            sys.exit()
    for i in range(len(keywords)):
        console_logger.info(f"Work has begun with: {keywords[i]}")
        file_logger.debug(f"Work with: {keywords[i]}")
        amount = accounting_for_downloads(url, keywords[i], headers)
        console_logger.info(f"{amount} images of a {keywords[i]} have been downloaded")
        file_logger.info(f"{amount} images of a {keywords[i]} have been downloaded")


if __name__ == "__main__":
    keys = sys.argv
    if len(keys) == 0:
        console_logger.info("Keywords are not specified, working with \"polar bear\", \"brown bear\"")
        file_logger.info("Keywords are not specified, working in default mode")
        keys = ["polar bear, brown bear"]
    image_download(URL, keys, HEADERS)
