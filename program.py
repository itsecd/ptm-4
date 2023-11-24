import os
from csv import reader
from email import iterators
from random import sample
from shutil import copyfile
from typing import Optional


class Iterator_1:
    '''Iterates images from source dataset'''
    def __init__(self, full_path: str, class_name: str) -> None:
        '''Constructor'''
        self.path_ = os.path.join(full_path, class_name)
        self.names = os.listdir(self.path_)
        names_ = self.names.copy()
        for i in names_:
            if not ".jpg" in i:
                self.names.remove(i)
        self.limit = len(self.names)
        self.counter = 0

    def __iter__(self) -> iterators:
        '''For iterating in a for loop'''
        return self

    def __next__(self) -> str:
        '''Returning an iterator and moving on to the next one'''
        if self.counter < self.limit:
            self.counter += 1
            return os.path.join(self.path_, self.names[self.counter - 1])
        else:
            raise StopIteration


class Iterator_2:
    '''iterating images organized as in item 2'''
    def __init__(self, full_path: str, class_name: str) -> None:
        '''Constructor'''
        self.path_to_folder = full_path
        self.names = os.listdir(full_path)
        names_ = self.names.copy()
        for i in names_:
            if not class_name in i:
                self.names.remove(i)
        self.limit = len(self.names)
        self.counter = 0

    def __iter__(self) -> iterators:
        '''For iterating in a for loop'''
        return self

    def __next__(self) -> str:
        '''Returning an iterator and moving on to the next one'''
        if self.counter < self.limit:
            self.counter += 1
            return os.path.join(self.path_to_folder, self.names[self.counter - 1])
        else:
            raise StopIteration


class Iterator_3:
    '''iterating images organized as in item 3'''
    def __init__(self, full_path: str, class_name: str) -> None:
        '''Constructor'''
        self.path_img = []

        with open(os.path.join(full_path, "annotation.csv")) as File:
            reader_ = reader(File, delimiter=" ")
            for it in reader_:
                if it[2] == class_name:
                    self.path_img.append(it[0])
        
        self.limit = len(self.path_img)
        self.counter = 0

    def __iter__(self) -> iterators:
        '''For iterating in a for loop'''
        return self

    def __next__(self) -> str:
        '''Returning an iterator and moving on to the next one'''
        if self.counter < self.limit:
            self.counter += 1
            return self.path_img[self.counter - 1]
        else:
            raise StopIteration


def class_img(animal: str, names_list: list, n: int) -> str:
    '''Specifies the image class'''
    if animal == "cat" or animal == "dog":
        return animal
    else:
        return (names_list[n])[0:3]


def create_csv(path_to_csv: str, path_fol: str, animal: str) -> None:
    '''Creates a csv file for items 1 and 2 of Lab №2'''
    path_ = os.path.join(path_fol, animal)
    names_list = os.listdir(path_)
    with open(path_to_csv, 'a') as file_csv:
        for index, image in enumerate(names_list):
            if ".jpg" in image:
                abspath = os.path.join(path_, image)
                class_ = class_img(animal, names_list, index)
                rel_path = os.path.join(animal, image)
                line = abspath + " " + rel_path + " " + class_ + "\n"
                file_csv.write(line)


def create_dir(name_dir: str) -> str:
    '''Create a folder'''
    path_ = os.path.join("dataset", name_dir)
    if not os.path.isdir(path_):
        os.mkdir(path_)
    return path_


def copy_dataset(path_fol: str, ndp: str, animal: str) -> None:
    '''Copying the dataset in accordance with item 2 of laboratory №2'''
    path_ =  os.path.join(path_fol, animal)
    names = os.listdir(path_)
    for item in names:
        if ".jpg" in item:
            old_location = os.path.join(path_, item)
            new_location = os.path.join(ndp, f'{animal}_{item}')
            copyfile(old_location, new_location)


def randnames_create_csv(ndp: str) -> None:
    '''Copying the dataset in accordance with item 3 of laboratory №2'''
    names_list = os.listdir(ndp)
    rand_num_array = sample(range(0, 10001), len(names_list))
    name_csv = "annotation.csv"
    with open(os.path.join(ndp, name_csv), 'w') as file_csv:
        for index, file in enumerate(names_list):
            if ".jpg" in file:
                old_name = os.path.join(ndp, file)
                new_name = os.path.join(ndp, f'{rand_num_array[index]}.jpg')
                os.rename(old_name, new_name)
                line = new_name + " " + f"{rand_num_array[index]}.jpg" + " " + file[0:3] + "\n"
                file_csv.write(line)


def iterator(class_name: str) -> Optional[str]:
    '''Function "iterator" for item 4 of laboratory No. 2'''
    path_ = os.path.join("dataset", class_name)
    names = os.listdir(path_)
    for i in range(len(names)):
        if ".jpg" in names[i]:
            path_file = os.path.join(path_, names[i])
            yield (path_file)
    return None