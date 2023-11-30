import os
import random
import string
import time

import logging
import requests
from bs4 import BeautifulSoup
from enum import Enum
from PIL import ImageChops, Image
from tqdm import tqdm

PBEAR_PATH = "E:\dataset\polarbears"
BBEAR_PATH = "E:\dataset\\brownbears"
COUNT_FIND = 1050


class Bears(Enum):
    POLAR_BEAR = "polar bear"
    BROWN_BEAR = "brown bear"


def find_images(count_imgs: int, path: str, name: str) -> None:
    """
    Находит картинки на Яндексе по запросу.

    Аргументы:
        count_imgs(int): количество картинок для поиска
        path(str): путь сохранения картинок
        name(str): имя запроса
    """
    for i in tqdm(range(3, 999), desc="Страница ", colour="green"):
        letters = string.ascii_lowercase
        rand_string = "".join(random.sample(letters, 10))
        _headers = {"User-Agent": rand_string}
        url = f"https://yandex.ru/images/search?p={i}&text={name}&"
        try:
            html_page = requests.get(url, headers=_headers)
            soup = BeautifulSoup(html_page.text, "html.parser")
        except Exception as err:
            logging.error(f"Невалидный URL: {err}")
        src_list = []
        for link in soup.find_all("img", class_="serp-item__thumb justifier__thumb"):
            src_list.append(link.get("src"))
        logging.info("Получены адреса картинок для загрузки.")
        count = get_images(count_imgs, path, src_list)
        logging.info(f"Загружено {count} картинок...")
        if count == count_imgs:
            return


def get_images(count_imgs: int, path: str, src_list: list) -> int:
    """
    Сохраняет найденные картинки по заданному пути

    Аргументы:
        count_imgs(int): количество картинок для поиска
        path(str): путь сохранения картинок
        src_list(list): список адресов картинок для загрузки
        
    Возвращаемое значение: 
        int: количество загруженных картинок
    """
    count = 0
    for img_url in tqdm(src_list, desc="Скачивание картинок ", colour="green"):
        if img_url.find("n=13") != -1:
            try:
                source = "https:" + img_url
                picture = requests.get(source)
                name_file = str(count)
                fpicture = open(path + "/" + name_file.zfill(4) + ".jpg", "wb")
                fpicture.write(picture.content)
                fpicture.close()
                time.sleep(0.25)
                count += 1
                if count == count_imgs:
                    return count
                return count
            except Exception as err:
                logging.error(f"Ошибка при скачивании картинки: {err}")


def img_compare(img1: str, img2: str) -> tuple or None:
    """
    Сравнивает две картинки

    Аргументы:
        img1(str): путь первой картинки
        img2(str): путь второй картинки

    Возвращаемое значение:
        tuple or None: tuple, если картинки разные, None - одинаковые
    """
    try:
        image_1 = Image.open(img1)
        image_2 = Image.open(img2)
        result = ImageChops.difference(image_1, image_2).getbbox()
        return result
    except Exception as err:
        logging.error(f"Не удалось сравнить картинки: {err}")


def check_images(path: str, count: int) -> int:
    """
    Проверяет, есть ли одинавковые картинки, и возвращает количество картинок для дозагрузки

    Аргументы:
        path(str): путь до картинок
        count(int): количество картинок для загрузки

    Возвращаемое значение:
        int: количество удалённых картинок
    """
    c = count
    images = []
    for filename1 in os.listdir(path):
        images.append(os.path.join(path, filename1))
    for fname1 in tqdm(images, colour="green"):
        for fname2 in images:
            if fname1 == fname2:
                continue
            if img_compare(fname1, fname2) == None:
                os.remove(fname2)
                logging.info(f"Найдены идентичные картинки: {fname1} and {fname2}")
                c -= 1
    return count - c


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="prog_logs.log", filemode="w")
    get_images(COUNT_FIND, PBEAR_PATH, Bears.POLAR_BEAR)
    print("Следующий этап")
    get_images(COUNT_FIND, BBEAR_PATH, Bears.BROWN_BEAR)
    new_count = check_images(PBEAR_PATH, COUNT_FIND)
    get_images(new_count, PBEAR_PATH, Bears.POLAR_BEAR)
    print("Следующий этап")
    new_count = check_images(BBEAR_PATH, COUNT_FIND)
    get_images(new_count, BBEAR_PATH, Bears.BROWN_BEAR)
