import argparse
import csv
import os
import random
import shutil
import tqdm


def copy_dataset(directory_obj: str, c_directory_obj: str, name: str) -> None:
    """Copies all files from one folder to another.
    Args:
        directory_obj (str): The path of the source folder.
        c_directory_obj (str): Folder path to copy.
        name (str): Object class.
    """
    c_directory_obj1 = f"{c_directory_obj}dataset_3"
    if not os.path.isdir(c_directory_obj1):
        os.makedirs(c_directory_obj1)
    r_list = list(range(1, 10001))
    random.shuffle(r_list)
    r_list = [str(i) for i in r_list]
    c_data = os.listdir(c_directory_obj1)
    if c_data:
        c_data = list(
            map(lambda sub: int(''.join([ele for ele in sub if ele.isnumeric()])), c_data))
        c_data = [str(i) for i in c_data]
        for i in c_data:
            r_list.remove(i)
    j = 0
    copy_list = []
    data = os.listdir(directory_obj)
    for i in tqdm.tqdm(data):
        so = str(r_list[j])
        so = f"{name}.{so}"
        copy_list.append(so)
        shutil.copy(directory_obj + "\\" + i,
                    c_directory_obj1 + "\\" + so + '.jpeg')
        j += 1
    write_csv_copy(c_directory_obj1, name, copy_list)


def write_csv_copy(c_directory_obj: str, name: str, copy_list: list) -> None:
    """Writes the absolute and relative path of the image to csv.
    Args:
        c_directory_obj (str): Folder path to copy.
        name (str): Object class.
        copy_list (list): Numbers of copied objects.
    """
    file = f"{c_directory_obj}rand.csv"
    f = open(file, "a", encoding="utf-8", newline="")
    f_writer = csv.DictWriter(
        f, fieldnames=["Absolut_path", "Relative_patch", "Class"], 
        delimiter="|")
    r_directory_obj = "dataset_3"
    for i in copy_list:
        f_writer.writerow({"Absolut_path": c_directory_obj + "\\" + i,
                          "Relative_patch":  r_directory_obj + "\\" + i, 
                          "Class": name})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-directory', type=str)
    parser.add_argument('-c_directory', type=str)
    parser.add_argument('-name', type=str)
    try:
        args = parser.parse_args()
        copy_dataset(args.directory, args.c_directory, args.name)
    except Exception as e:
        print("Произошла ошибка:", e)
