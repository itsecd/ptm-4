import os
import time
import requests
from bs4 import BeautifulSoup

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}


def Search_Images(Limit_of_find: int) -> None:
    num_page = 0
    i = 0
    os.system('cls')
    print("=" * 100)
    print("\nStart searching images with zebra and bay horse\n")
    print("=" * 100)
    while True:
        first_url = f"https://yandex.ru/images/search?p={num_page}&text=zebra&uinfo=sw-1536-sh-864-ww-760-wh-754-pd-1.25-wp-16x9_1920x1080&lr=51&rpt=image"
        second_url = f"https://yandex.ru/images/search?p={num_page}&from=tabbar&text=bay%20horse&lr=51&rpt=image&uinfo=sw-1920-sh-1080-ww-1220-wh-970-pd-1-wp-16x9_1920x1080"
        num_page += 1

        first_response = requests.get(first_url, headers=headers)
        first_soup = BeautifulSoup(first_response.content, 'html.parser')

        for tos in range(1, 61, 1):
            time.sleep(1)
            os.system('cls')
            print('=' * tos)
            print("\n\nLoading", tos)

        second_response = requests.get(second_url, headers=headers)
        second_soup = BeautifulSoup(second_response.content, 'html.parser')

        first_list_of_src = []
        second_list_of_src = []

        for link in first_soup.find_all("img"):
            first_list_of_src.append(link.get("src"))
        for link in second_soup.find_all("img"):
            second_list_of_src.append(link.get("src"))

        Save_Images_With_Zebra(first_list_of_src, i)
        i = Save_Images_With_Bay_Horse(second_list_of_src, Limit_of_find, i)


def Save_Images_With_Zebra(list_of_src: str, i: int) -> None:
    os.system('cls')
    print("\tSave zebra")
    index = i
    for url in list_of_src:
        if url.find("n=13") != -1:
            try:
                link = "https:" + url
                img = requests.get(link)
                name_of_file = str(index)
                name_of_file = "dataset/zebra/" + \
                    name_of_file.zfill(4) + ".jpg"
                img_option = open(name_of_file, "wb")
                img_option.write(img.content)
                img_option.close()
                index += 1
                print("Save ", str(index).zfill(4))
            except:
                print("Error after ", index)
            link_option = open("dataset/zebra/zebra_link.txt", "a")
            link_option.write(url + "\n")
            link_option.close()


def Save_Images_With_Bay_Horse(list_of_src: str, Limit_of_find: int, i: int) -> int:
    os.system('cls')
    print("\tSave bay horse")
    for url in list_of_src:
        if url.find("n=13") != -1:
            try:
                link = "https:" + url
                img = requests.get(link)
                name_of_file = str(i)
                name_of_file = "dataset/bay_horse/" + \
                    name_of_file.zfill(4) + ".jpg"
                img_option = open(name_of_file, "wb")
                img_option.write(img.content)
                img_option.close()
                i += 1
                print("Save ", str(i).zfill(4))
            except:
                print("Error after ", i)
            link_option = open("dataset/bay_horse/bay_horse_link.txt", "a")
            link_option.write(url + "\n")
            link_option.close()
            if i == Limit_of_find:
                Finish()
    return i


def Finish() -> None:
    print("\nProgram has finished!\n")
    exit(0)


def main() -> None:
    if not os.path.isdir("dataset"):
        os.mkdir("dataset")
        os.mkdir("dataset/zebra")
        os.mkdir("dataset/bay_horse")
    Limit_of_find = 1050
    Search_Images(Limit_of_find)


if __name__ == '__main__':
    main()
