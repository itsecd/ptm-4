import argparse
import csv
import os
import shutil
import tqdm


def copy_dataset(directory_obj: str, c_directory_obj: str, name: str) -> None:
    """Copies all files from one folder to another.
    Args:
        directory_obj (str): The path of the source folder.
        c_directory_obj (str): Folder path to copy.
        name (str): Object class.
    """
    c_directory_obj1 = f"{c_directory_obj}dataset_2"
    if not os.path.isdir(c_directory_obj1):
        os.makedirs(c_directory_obj1)
    data = os.listdir(directory_obj)
    for i in tqdm.tqdm(data):
        shutil.copy(directory_obj + "\\" + i,
                    c_directory_obj1 + "\\" + name + "_" + i)
    write_csv_copy(directory_obj, c_directory_obj1, name)


def write_csv_copy(directory_obj: str, c_directory_obj: str, name: str) -> None:
    """Writes the absolute and relative path of the image to csv.
    Args:
        directory_obj (str): The path of the source folder.
        c_directory_obj (str): Folder path to copy.
        name (str): Object class.
    """
    data = os.listdir(directory_obj)
    r_directory_obj = "dataset_2"
    file = f"{c_directory_obj}copy.csv"
    with open(file, "a", encoding="utf-8", newline="") as f:
        f_writer = csv.DictWriter(f,
                                  fieldnames=["Absolut_path",
                                              "Relative_patch",
                                              "Class"],
                                  delimiter="|")
        for i in data:
            f_writer.writerow({"Absolut_path": c_directory_obj + "\\" + name + "_" + i,
                               "Relative_patch":  r_directory_obj + "\\" + name + "_" + i,
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
