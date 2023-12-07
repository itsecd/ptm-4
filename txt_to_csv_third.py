import csv
import os
import pathlib
from random import Random, random
from datetime  import datetime as dt
import logging


logging.basicConfig(level="DEBUG")


class Comment:

    def __init__(self):  # по умолчанию
        self.name = None
        self.comment = None
        self.mark = None


def create_repo() -> None:
    """Creates repository in current folder
    """
    os.mkdir("dataset_copy")
    for i in range(1, 6):
        try:
            os.mkdir("dataset_copy/"+str(i))
            logging.debug(f"Репозитория для {i} оценки создан")
        except:
            logging.error(f"При создании папки dataset/copy/{i} произошла ошибка. {dt.now()}")
    logging.info(f"Все репозитории для оценок созданы успешно")


def save_comments(data: Comment, foldername: str) -> None:
    """Saves comments give

    Args:
        data (Comment):  List of comments
        foldername (str): filename
    """
    for i in range(1, len(data)):

        used_digits = [0]
        random = Random()
        digit = 0

        while digit in used_digits:
            digit = random.randint(1, 10000)
        try:
            file = open(foldername+f'/{digit:04}'+'.txt', "w", encoding="utf-8")
            file.write(data[i].name)
            file.write('\n')
            file.write(data[i].comment)
            file.close
            logging.debug(f"Сохранение данных в файл {foldername}/{digit:04}.txt в функции save_comment прошло УСПЕШНО. {dt.now()}")
        except:
            logging.error(f"Ошибка при сохранении данных в файл {foldername}/{digit:04}.txt в функции save_comment. {dt.now()}")

        used_digits.append(digit)


def write_dataset(dataset: str) -> None:
    """Writes dataset

    Args:
        dataset (str): New dataset's path
    """
    try:
        one_data = [el for el in dataset if el.mark < 2.0]
        save_comments(one_data, "dataset_copy/1")

        two_data = [el for el in dataset if el.mark < 3.0 and el.mark >= 2.0]
        save_comments(two_data, "dataset_copy/2")

        three_data = [el for el in dataset if el.mark < 4.0 and el.mark >= 3.0]
        save_comments(three_data, "dataset_copy/3")

        four_data = [el for el in dataset if el.mark < 5.0 and el.mark >= 4.0]
        save_comments(four_data, "dataset_copy/4")

        five_data = [el for el in dataset if el.mark == 5.0]
        save_comments(five_data, "dataset_copy/5")
        logging.info(f"Запись всех файлов прошла успешно в функции write_dataset. {dt.now()}")
    except:
        logging.info("Ошибка произошла в см на логи выше")


def create_copy(path: str) -> None:
    """Creates copy of dataset

    Args:
        path (str): Path to dataset
    """
    dataset = get_dataset(path)
    create_repo()
    write_dataset(dataset)


def get_dataset(path: str) -> Comment:
    """Reads all data from dataset and returns it as Comment class's ocjects

    Args:
        path (str): path to dataset

    Returns:
        Comment: List of comments
    """
    dataset = list()
    for folder_num in range(1, 6):

        folder_path = path+'/'+str(folder_num)
        num_of_files = sum(os.path.isfile(os.path.join(folder_path, f))
                           for f in os.listdir(folder_path)) + 1

        for file_num in range(1, num_of_files):
            path_to_file = folder_path+f'/{(file_num):04}'+'.txt'
            comment = Comment()
            buffer_comment_text = ""
            line_counter = 0
            try: 
                with open(path_to_file, 'r', encoding='utf-8')as file:
                    while True:
                        line = file.readline()
                        if not line:
                            break
                        if line_counter == 0:
                            comment.name = line
                        else:
                            buffer_comment_text += line

                        line_counter += 1   
                logging.debug(f"Отработан корректно {path_to_file}. {dt.now()}")
            except:
                logging.error(f"Ошибка открытия файла {path_to_file}. {dt.now()}")

            buffer_comment_text = buffer_comment_text.replace(u'\xa0', u' ')

            comment.mark = folder_num
            comment.comment = buffer_comment_text.strip()

            dataset.append(comment)

    return dataset


def get_paths_to_files(path_to_dataset: str) -> str:
    """Reads paths to files in dataset

    Args:
        path_to_dataset (str): Path to source

    Returns:
        str: List of paths to files
    """
    paths_to_files = list()

    for folder_num in range(1, 6):
        folder_path = path_to_dataset+'/'+str(folder_num)
        #num_of_files = sum(os.path.isfile(os.path.join(folder_path, f)) for f in os.listdir(folder_path)) + 1

        currentDirectory = pathlib.Path('./dataset_copy'+f'/{folder_num}')
        for currentFile in currentDirectory.iterdir():
            logging.info(f"В функции get_paths_to_files {currentFile} {dt.now()}")
            paths_to_files.append(currentFile)

    return paths_to_files


def write_as_csv(path_to_dataset: str, paths_to_files: str) -> None:
    """Writes all data as CSV

    Args:
        path_to_dataset (str): Path to surce
        paths_to_files (str): Paths to files
    """
    try:
        with open("dataset_csv_third.csv", "w+", encoding='utf-8', newline='') as file:
            csv_file = csv.writer(file, delimiter=';')
            csv_file.writerow(["Absolute path", "Relative path", "Class"])

            for i in range(0, len(paths_to_files)):
                paths_to_files[i] = str(paths_to_files[i])
                csv_file.writerow([f'{path_to_dataset + paths_to_files[i]}',
                                  paths_to_files[i], os.path.basename(paths_to_files[i])])
        logging.info(f"Все данные успешно были записаны в файл dataset_csv_third.csv... {dt.now()}")
    except:
        logging.error(f"В функции write_as_csv при записи в csv файл произошла ошибка. открывался файл: dataset_csv_third.csv...  {dt.now()}")

if __name__ == '__main__':

    path_to_dataset = os.path.join( 'application_programming_first_lab_and_dataset','dataset')

    create_copy(path_to_dataset)

    path_new_dataset = os.path.abspath("./dataset_copy")
    paths_to_files = get_paths_to_files(path_new_dataset)

    write_as_csv(path_new_dataset, paths_to_files)

    logging.info(f"Работа данного скрипта завершена. {dt.now()}")
