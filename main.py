import os
import logging
from random_dataset import add_to_csv_and_to_dataset_random_number, find_path_txt_random
from copy_dataset import find_path_txt, copy_dataset_new, add_csv


formatter = '[%(asctime)s: %(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, filename="logger.log", filemode="w", format=formatter)


def main_1(path_dataset: str):
    path_txt_old = find_path_txt(path_dataset, '\\')
    path_txt_new = find_path_txt(path_dataset, '_')
    copy_dataset_new(path_dataset, path_txt_old, path_txt_new)
    add_csv(path_dataset, path_txt_new)


def main_2(path_dataset: str):
    paths_txt = find_path_txt_random(path_dataset)
    add_to_csv_and_to_dataset_random_number(path_dataset, paths_txt)

if __name__ == "__main__":
    logging.info('Start work of program')
    path_dataset = os.path.abspath('dataset')
    main_1(path_dataset)
    main_2(path_dataset)
    logging.info('final work of program')