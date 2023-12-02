import os
import csv
import get_way
import logging


def write_in_file(name_class: str, number: int) -> None:
    '''
    запись в csv-файл(абсолютный путь/относительный путь/тег класса)
    '''
    with open("dataset.csv", "a", newline='', encoding='utf8') as file:
        printer = csv.writer(file, delimiter=";")
        printer.writerow(
            [os.path.abspath(get_way.create_download_relative_way(name_class, number)),
             get_way.create_download_relative_way(name_class, number),
             name_class]
        )


def create_annotation(folderpath: str) -> None:
    '''
    создание csv-файла
    поочерёдная запись в файл-аннотацию из папки download_data
    '''
    logging.basicConfig(filename='loginfo.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')
    logging.info("Start create csv file")
    try:
        num_files = len([f for f in os.listdir(folderpath + "/zebra")
                        if os.path.isfile(os.path.join(folderpath + "/zebra", f))])
        with open("dataset.csv", "w", newline='') as file:
            printer = csv.writer(file, delimiter=";", )
            printer.writerow(["The Absolute Way", "Relative Way", "Class"])
        for i in range(0, num_files):
            name_class = "zebra"
            way = f"{folderpath}/{name_class}/{str(i).zfill(4)}.jpg"
            if os.path.isfile(way):
                write_in_file(name_class, i)
            name_class = "bay_horse"
            way = f"{folderpath}/{name_class}/{str(i).zfill(4)}.jpg"
            if os.path.isfile(way):
                write_in_file(name_class, i)
    except FileExistsError:
        logging.error("ERROR! Func create_annotation can't open folder/file")
    logging.info("Finish create csv file")
