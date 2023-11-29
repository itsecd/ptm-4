import csv
import shutil
import os
def make_csv(name_csv: str) -> None:
    """Функция создает файл разрешения csv

    Args:
        name_csv (str): _название файла, который нужно создать_
    """
    with open(f"{name_csv}.csv", "w+", encoding="UTF-8", newline="") as file:
        csv_file = csv.writer(file, delimiter=";")
        csv_file.writerow(["Absolute path", "Relative path", "Class"])



def porting(name_abstract: str, new_csv: str) -> None:
    """Функция импортируют файлы из собранного датасета в новый датасет. Файлы именуются по принципу "класс_Имяфайла.jpg"
        так же функция создает новый csv файл для нового датасета

    Args:
        name_abstract (str): имя csv из которого берем путь, имя и класс
        new_csv (str): имя csv файла в которой импортируем новый путь, имя и класс
    """
    try:
        os.mkdir("dataset")
    except:
        print("====ФАЙЛ ИМЕЕТСЯ====")
    with open(f"{name_abstract}.csv", newline="") as file:
        read = csv.DictReader(file, delimiter=";")
        with open(f"{new_csv}.csv", "a", encoding="UTF-8", newline="") as file1:
            csv_file = csv.writer(file1, delimiter=";")
            for row in read:
                FROM = row["Absolute path"]
                a = FROM.split("/")
                TO = f"dataset/{a[-2]}_{a[-1]}"
                shutil.copyfile(FROM, TO)
                name_class = row["Class"]

                fullWay = os.getcwd() + f"\dataset\{a[-2]}_{a[-1]}"
                Way = f"dataset\{a[-2]}_{a[-1]}"
                csv_file.writerow([fullWay, Way, name_class])