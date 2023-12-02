import json
import my_logger


def read_json(variant: str) -> dict:
    """Читаем начальные параметры, вовзращаем словарь"""
    result = {
        "hash": '',
        "bins": [],
        "last_num": '',
        "hash_format": ''
    }
    with open("parametrs.json", "r") as file:
        data = json.load(file)
        result["hash"] = data[variant]["hash"]
        result["last_num"] = data[variant]["last_numbers"]
        for i in range(len(data[variant]["bins"])):
            result["bins"].append(data[variant]["bins"][i])
        result["hash_format"] = data[variant]["hash_format"]
    logger = my_logger.My_log(__file__).get_logger()
    logger.debug("The settings have been uploaded successfully")
    return result
