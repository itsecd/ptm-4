import os
import csv
import shutil
from typing import List
import logging


def add_csv (path_dataset: str, paths_txt: str) -> None:
    '''
    Создаёт и записывает файл аннотацию для определния классов файлов из папки 
    '''
    file_name = 'copy_dataset.csv'
    #создаём  или открываем файл аннотацию для заполнения
    try:
        with open(file_name,'w+', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=' ')
            writer.writerow(["Absolute path", "Relative path", "Class"])
        
            #проходимся по нашим именам и записываем их в аннотацию
            for i in range (len(paths_txt)):
                class_txt = os.path.join(str(paths_txt[i]))
                class_name = 'bad'
                if class_txt [0 : 4] == ('good'):
                    class_name = 'good'
                writer.writerow([f'{os.path.join(path_dataset, str(paths_txt[i])).replace(" ","")}', 
                    os.path.join('..', 'dataset', f'{(str(paths_txt[i])).replace(" ","")}'), f'{ class_name}'])
    except Exception as err:
        logging.error(f'Error with the csv {err}')
    logging.info(f'Information is recorded in  {file_name}')
    

            
def copy_dataset_new(path_dataset: str, path_txt_old: str, path_txt_new: str) -> None:
    '''
    Создаёт и заполняет папку-копию dataset без классов c файлами "class_номер"
    '''

    name_folder = "copy_dataset"
    #создаём папку
    if not os.path.isdir(name_folder):
        logging.info(f'Сreating a folder "{name_folder}"')
        os.mkdir(name_folder)
    else:
        logging.info(f'A folder {name_folder} already exists.')
    logging.info('Let is start recording')
    #заполняем папку
    try:
        for i in range(len(path_txt_old)):
            shutil.copyfile(os.path.join(path_dataset, str(path_txt_old[i])), os.path.join(name_folder, str(path_txt_new[i])))
    except Exception as err:
         logging.error(f'Error {err} with folder {name_folder}')


def find_path_txt (path_dataset, delimiter) -> List[str]:
    '''
    Функция формирует и возвращает список из путей к текстовым файлам
    '''
    paths_txt = []
    class_list = ('bad', 'good')

    #Находим длину список имён файлов
    try:
        for folder_name in class_list:
            count = len([f for f in os.listdir(os.path.join(path_dataset, folder_name)) if os.path.join(path_dataset, folder_name, f)])
            logging.info(f'The path to the {folder_name} has been found')
            #записываем пути
            for j in range (count):
                path_txt = folder_name + delimiter +  f'{(j): 05}' + '.txt'
                print(f'{folder_name}: {(j): 05}')
                paths_txt.append(path_txt.replace(" ",""))
    except Exception as err:
        logging.error(f'Error {err} ')
    return paths_txt


def copy_dataset_add_csv() -> None:
    """
    функция, выполняющая копирование в новый dataset и делающая csv-файл к нему
    """
    path_dataset = os.path.abspath('dataset')
    path_txt_old = find_path_txt(path_dataset, '\\')
    path_txt_new = find_path_txt(path_dataset, '_')
    copy_dataset_new(path_dataset, path_txt_old, path_txt_new)
    add_csv(path_dataset, path_txt_new)