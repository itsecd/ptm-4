import os
import logging
from csv import reader
from email import iterators
from random import sample
from shutil import copyfile
from typing import Optional

logging.getLogger().setLevel(logging.INFO)


class Iterator_1:
    '''Iterates images from source dataset'''
    def __init__(self, full_path: str, class_name: str) -> None:
        '''Constructor'''
        self.__class_name = class_name
        self.__path = os.path.join(full_path, class_name)
        self.__names = os.listdir(self.__path)
        names = self.__names.copy()
        for i in names:
            if not ".jpg" in i:
                self.__names.remove(i)
        self.__limit = len(self.__names)
        self.__counter = 0
        logging.info(
            "Обьект класса 'Iterator_1', хранящий имена содержимого папки "
            f"{class_name} по пути {self.__path}, был создан успешно"
        )

    def __iter__(self) -> iterators:
        '''For iterating in a for loop'''
        return self

    def __next__(self) -> str:
        '''Returning an iterator and moving on to the next one'''
        if self.__counter < self.__limit:
            self.__counter += 1
            logging.info(
                f"В классе 'Iterator_1' итерируется: "
                f"{self.__names[self.__counter - 1]}"
            )
            return os.path.join(self.__path, self.__names[self.__counter - 1])
        else:
            logging.info(
                "Итерация объекта класса 'Iterator_1', хранящего имена содержимого "
                f"папки {self.__class_name} по пути {self.__path}, была завершена"
            )
            raise StopIteration


class Iterator_2:
    '''iterating images organized as in item 2'''
    def __init__(self, full_path: str, class_name: str) -> None:
        '''Constructor'''
        self.__class_name = class_name
        self.__path_to_folder = full_path
        self.__names = os.listdir(full_path)
        names = self.__names.copy()
        for i in names:
            if not class_name in i:
                self.__names.remove(i)
        self.__limit = len(self.__names)
        self.__counter = 0
        logging.info(
            f"Обьект класса 'Iterator_2', хранящий элементы с подстрокой "
            f"{class_name} по пути {self.__path_to_folder}, был создан успешно"
        )

    def __iter__(self) -> iterators:
        '''For iterating in a for loop'''
        return self

    def __next__(self) -> str:
        '''Returning an iterator and moving on to the next one'''
        if self.__counter < self.__limit:
            self.__counter += 1
            logging.info(
                f"В классе 'Iterator_2' итерируется: "
                f"{self.__names[self.__counter - 1]}"
            )
            return os.path.join(self.__path_to_folder, self.__names[self.__counter - 1])
        else:
            logging.info(
                "Итерация объекта класса 'Iterator_2', хранящего элементы с подстрокой "
                f"{self.__class_name} по пути {self.__path_to_folder}, была завершена"
            )
            raise StopIteration


class Iterator_3:
    '''iterating images organized as in item 3'''
    def __init__(self, full_path: str, class_name: str) -> None:
        '''Constructor'''
        self.__class_name = class_name
        self.__path_img = []
        self.__path_to_csv = os.path.join(full_path, "annotation.csv")
        with open(self.__path_to_csv) as file:
            reader_ = reader(file, delimiter=" ")
            for it in reader_:
                if it[2] == class_name:
                    self.__path_img.append(it[0])
        self.__limit = len(self.__path_img)
        self.__counter = 0
        logging.info(
            f"Объект класса 'Iterator_3', хранящий пути к изображениям с меткой {class_name} "
            f"в csv-таблице, расположенной по пути {self.__path_to_csv}, был создан успешно"
        )

    def __iter__(self) -> iterators:
        '''For iterating in a for loop'''
        return self

    def __next__(self) -> str:
        '''Returning an iterator and moving on to the next one'''
        if self.__counter < self.__limit:
            self.__counter += 1
            logging.info(
                f"В классе 'Iterator_2' итерируется: "
                f"{self.__path_img[self.__counter - 1]}"
            )
            return self.__path_img[self.__counter - 1]
        else:
            logging.info(
                "Итерация объекта  класса 'Iterator_3', хранящего пути к изображениям "
                f"с меткой {self.__class_name} в csv-таблице, расположенной по пути "
                f"{self.__path_to_csv}, была завершена"
            )
            raise StopIteration


def class_img(animal: str, names_list: list, n: int) -> str:
    '''Specifies the image class'''
    if animal == "cat" or animal == "dog":
        logging.info(
            f"Функция 'class_img' вернула значение {animal}, переданное в ф-цию"
        )
        return animal
    else:
        animal = (names_list[n])[0:3]
        logging.info(
            f"Функция 'class_img' вернула значение {animal} из имени файла"
        )
        return animal


def create_csv(path_to_csv: str, path_dir: str, animal: str) -> None:
    '''Creates a csv file for items 1 and 2 of Lab №2'''
    path_ = os.path.join(path_dir, animal)
    names_list = os.listdir(path_)
    with open(path_to_csv, 'a') as file_csv:
        for index, image in enumerate(names_list):
            if ".jpg" in image:
                abspath = os.path.join(path_, image)
                class_ = class_img(animal, names_list, index)
                rel_path = os.path.join(animal, image)
                line = abspath + " " + rel_path + " " + class_ + "\n"
                file_csv.write(line)
    logging.info(
        "CSV-таблица с информацией об изображениях, находящихся"
        f" в папке {path_}, была создана успешно"
    )


def create_dir(name_dir: str) -> str:
    '''Create a folder'''
    path_ = os.path.join("dataset", name_dir)
    if not os.path.isdir(path_):
        os.mkdir(path_)
        logging.info(
            f"Папка с именем {name_dir}, успешно создана в {path_}"
        )
    else:
        logging.warning(
            f"Папка, находящаяся по пути {path_}, уже существует"
        )
    return path_


def copy_dataset(path_dir: str, new_data_path: str, animal: str) -> None:
    '''Copying the dataset in accordance with item 2 of laboratory №2'''
    path_ =  os.path.join(path_dir, animal)
    names = os.listdir(path_)
    for item in names:
        if ".jpg" in item:
            old_location = os.path.join(path_, item)
            new_location = os.path.join(new_data_path, f'{animal}_{item}')
            copyfile(old_location, new_location)
    logging.info(
        "Изображения были успешно скопированы"
        f" из {path_} в {new_data_path}"
    )
    


def randnames_create_csv(path_dir: str, name_csv: str) -> None:
    '''Copying the dataset in accordance with item 3 of laboratory №2'''
    names_list = os.listdir(path_dir)
    rand_num_array = sample(range(0, 10001), len(names_list))
    with open(os.path.join(path_dir, name_csv), 'w') as file_csv:
        for index, file in enumerate(names_list):
            if ".jpg" in file:
                old_name = os.path.join(path_dir, file)
                new_name = os.path.join(path_dir, f'{rand_num_array[index]}.jpg')
                os.rename(old_name, new_name)
                line = new_name + " " + f"{rand_num_array[index]}.jpg" + " " + file[0:3] + "\n"
                file_csv.write(line)
    logging.info(
        f"В папке {path_dir} были переименовыны изображения рандомными числами"
        " и создана csv-таблица с информацией об этих изображениях"
    )


def iterator(path_dir: str) -> Optional[str]:
    '''Function "iterator" for item 4 of laboratory No. 2'''
    names = os.listdir(path_dir)
    for i in range(len(names)):
        if ".jpg" in names[i]:
            path_file = os.path.join(path_dir, names[i])
            logging.info(
                f"Функция 'iterator' итерирует: {path_file}"
            )
            yield (path_file)
    logging.info(
        f"Функция 'iterator' завершила итерацию объектов из папки {path_dir}"
    )
    return None
