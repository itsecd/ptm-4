from pathlib import Path
import csv

def make_csv(name_csv: str) -> None:
    """Функция создает файл разрешения csv

    Args:
        name_csv (str): _название файла, который нужно создать_
    """
    with open(f"{name_csv}.csv", "w+", encoding="UTF-8", newline="") as file:
        csv_file = csv.writer(file, delimiter=";")
        csv_file.writerow(["Absolute path", "Relative path", "Class"])

def make_file_abstract(name_class: str, full_way: str, file_name: str) -> None:
    """Функция заполняет csv файл. В первый столбец полный путь файлов, второй столбец - путь

    Args:
        name_class (str)): _Название класса_
        full_way (str): _Полный путь к файлу_
        file_name (str): _имя файла разрешения csv_
    """
    full_way += name_class
    way = f"dataset/{name_class}/"
    folder = Path(full_way)
    if folder.is_dir():
        counter_files = len([1 for file in folder.iterdir()])  #
    with open(f"{file_name}.csv", "a", encoding="UTF-8", newline="") as file:
        csv_file = csv.writer(file, delimiter=";")
        for i in range(counter_files):
            csv_file.writerow([full_way + f"/{i}.jpg", way + f"{i}.jpg", name_class])