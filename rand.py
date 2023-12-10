import argparse
import csv
import logging
import os
import random
import shutil
import tqdm

formatter = '[%(asctime)s: %(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, filename="rand.log",
                    filemode="w", format=formatter)


def copy_dataset(directory_obj: str, c_directory_obj: str, name: str) -> None:
    """Copies all files from one folder to another.
    Args:
        directory_obj (str): The path of the source folder.
        c_directory_obj (str): Folder path to copy.
        name (str): Object class.
    """
    c_directory_obj1 = f"{c_directory_obj}dataset_3"
    if not os.path.isdir(c_directory_obj1):
        logging.info('There is no directory to copy')
        os.makedirs(c_directory_obj1)
        logging.info('Directory for copying has been created')
    r_list = list(range(1, 10001))
    random.shuffle(r_list)
    r_list = [str(i) for i in r_list]
    c_data = os.listdir(directory_obj)
    if c_data:
        c_data = list(
            map(lambda sub: int(''.join([ele for ele in sub if ele.isnumeric()])), c_data))
        c_data = [str(i) for i in c_data]
        for i in c_data:
            r_list.remove(i)
        logging.info('List of random numbers has been created')
    else:
        logging.error(f'File {directory_obj} is empty')
        raise
    j = 0
    copy_list = []
    data = os.listdir(directory_obj)
    for i in tqdm.tqdm(data):
        tmp = str(r_list[j])
        copy_list.append(tmp)
        j += 1
        src_path = os.path.join(directory_obj, i)
        dest_path = os.path.join(c_directory_obj1, f'{name}.{tmp}.jpeg')
        try:
            shutil.copy(src_path, dest_path)
        except Exception as err:
            logging.error(f'Error copying file {i}: {err}')
    logging.info(f'All files copied in {c_directory_obj1}')
    write_csv_copy(c_directory_obj1, name, copy_list)


def write_csv_copy(c_directory_obj: str, name: str, copy_list: list) -> None:
    """Writes the absolute and relative path of the image to csv.
    Args:
        c_directory_obj (str): Folder path to copy.
        name (str): Object class.
        copy_list (list): Numbers of copied objects.
    """
    file = f"{c_directory_obj}rand.csv"
    try:
        with open(file, 'a', encoding='utf-8', newline='') as f:
            f_writer = csv.DictWriter(f,
                                      fieldnames=['Absolut_path',
                                                  'Relative_patch',
                                                  'Class'],
                                      delimiter='|')
            r_directory_obj = 'dataset_3'
            for i in copy_list:
                abs_path = os.path.join(c_directory_obj, i)
                rel_path = os.path.join(r_directory_obj, i)
                f_writer.writerow({"Absolut_path": abs_path,
                                   "Relative_patch": rel_path,
                                   "Class": name})
    except Exception as err:
        logging.error(f'Error with the csv: {err}')
    logging.info(f'All names are written in {file}')


if __name__ == "__main__":
    logging.info('Start of program')
    parser = argparse.ArgumentParser()
    parser.add_argument('-directory', type=str)
    parser.add_argument('-c_directory', type=str)
    parser.add_argument('-name', type=str)
    try:
        args = parser.parse_args()
        copy_dataset(args.directory, args.c_directory, args.name)
    except Exception as err:        
        logging.error(f'Error in main: {err}')
    logging.info('End of program')    
