import os
import string
import time
from bs4 import BeautifulSoup
import requests
from re import sub
import random
from PIL import ImageChops, Image
from tqdm import tqdm


if not os.path.isdir("E:\dataset"):
    os.mkdir("E:\dataset")

if not os.path.isdir("E:\dataset\\brownbears"):
    os.mkdir("E:\dataset\\brownbears")

if not os.path.isdir("E:\dataset\polarbears"):
    os.mkdir("E:\dataset\polarbears")

PBEAR_PATH = "E:\dataset\polarbears"
BBEAR_PATH = "E:\dataset\\brownbears"


def get_images(count_imgs, path, name):
    count = 0

    for i in tqdm(range(3, 999), desc="Страница ", colour="green"):
        letters = string.ascii_lowercase
        rand_string = "".join(random.sample(letters, 10))
        _headers = {"User-Agent": rand_string}

        url = f"https://yandex.ru/images/search?p={i}&text={name}&"
        html_page = requests.get(url, headers=_headers)

        soup = BeautifulSoup(html_page.text, "html.parser")

        src_list = []

        for link in soup.find_all("img", class_="serp-item__thumb justifier__thumb"):
            src_list.append(link.get("src"))

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
                        return

                except Exception:
                    print("Error in: ", count)


def img_compare(img1, img2):
    image_1 = Image.open(img1)
    image_2 = Image.open(img2)
    result = ImageChops.difference(image_1, image_2).getbbox()
    return result


def check_images(path, count):
    c = count
    images = []
    for filename1 in os.listdir(path):
        images.append(os.path.join(path, filename1))

    for fname1 in tqdm(images, colour="green"):
        for fname2 in images:
            if fname1 == fname2:
                continue
            if img_compare(fname1, fname2) == None:
                print(fname1, fname2)
                os.remove(fname2)
                c -= 1
    return count - c


count_find = 1050

get_images(count_find, PBEAR_PATH, "polar bear")

print("Следующий этап")

get_images(count_find, BBEAR_PATH, "brown bear")

new_count = check_images(PBEAR_PATH, count_find)
get_images(new_count, PBEAR_PATH, "polar bear")

print("Следующий этап")

new_count = check_images(BBEAR_PATH, count_find)
get_images(new_count, BBEAR_PATH, "brown bear")
