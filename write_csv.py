import argparse
import csv
import os


def write_csv(directory_obj: str, file: str, name: str) -> None:
    """Writes the absolute and relative path of the image to csv.
    Args:
        directory_obj (str): Full path to the folder.
        file (str): The path to the file to save.
        name (str): Object class.
    """
    file = f"{file}annotation.csv"
    f = open(file, "a", encoding="utf-8", newline="")
    f_writer = csv.DictWriter(f, 
                              fieldnames=["Absolut_path", 
                                          "Relative_patch", 
                                          "Class"], 
                              delimiter="|")
    data = os.listdir(directory_obj)
    r_directory_obj = "dataset"
    for i in data:
        f_writer.writerow({"Absolut_path": directory_obj + "\\" + i, 
                           "Relative_patch":  r_directory_obj + "\\" + name + "\\" + i, 
                           "Class": name})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-directory', type=str)
    parser.add_argument('-annotation', type=str)
    parser.add_argument('-name', type=str)
    try:
        args = parser.parse_args()
        write_csv(args.directory, args.annotation, args.name)
    except Exception as e:
        print("Произошла ошибка:", e)
