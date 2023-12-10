import argparse
import csv
import logging
import os
import shutil
import tqdm

formatter = '[%(asctime)s: %(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, filename="copying.log", filemode="w", format=formatter)


def copy_dataset(directory_obj: str, c_directory_obj: str, name: str) -> None:
    """Copies all files from one folder to another.
    Args:
        directory_obj (str): The path of the source folder.
        c_directory_obj (str): Folder path to copy.
        name (str): Object class.
    """
    c_directory_obj1 = f'{c_directory_obj}dataset_2'
    if not os.path.isdir(c_directory_obj1):
        logging.info('There is no directory to copy')
        os.makedirs(c_directory_obj1)
        logging.info('Directory for copying has been created')
    data = os.listdir(directory_obj)
    for i in tqdm.tqdm(data):
        src_path = os.path.join(directory_obj, i)
        dest_path = os.path.join(c_directory_obj1, f'{name}_{i}')
        try:
            shutil.copy(src_path, dest_path)
        except Exception as err:
            logging.error(f'Error copying file {i}: {err}')
    logging.info(f'All files copied in {c_directory_obj1}')
    write_csv_copy(directory_obj, c_directory_obj1, name)


def write_csv_copy(directory_obj: str, c_directory_obj: str, name: str) -> None:
    """Writes the absolute and relative path of the image to csv.
    Args:
        directory_obj (str): The path of the source folder.
        c_directory_obj (str): Folder path to copy.
        name (str): Object class.
    """
    data = os.listdir(directory_obj)
    r_directory_obj = 'dataset_2'
    file = f'{c_directory_obj}copy.csv'
    try:
        with open(file, 'a', encoding='utf-8', newline='') as f:
            f_writer = csv.DictWriter(f,
                                      fieldnames=['Absolut_path',
                                                  'Relative_patch',
                                                  'Class'],
                                      delimiter='|')
            for i in data:
                abs_path = os.path.join(c_directory_obj, f'{name}_{i}')
                rel_path = os.path.join(r_directory_obj, f'{name}_{i}')
                f_writer.writerow({'Absolut_path': abs_path,
                                   'Relative_patch': rel_path,
                                   'Class': name})    
    except Exception as err:
        logging.error(f'Error with the csv: {err}')
    logging.info(f'All names are written in {file}')    


if __name__ == '__main__':
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
