import argparse as argp
import json
import re
from tqdm import tqdm
import logging
from typing import Any, Dict

# Set up logging
def setup_logging():
    logging.basicConfig(filename='validation.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to calculate SNILS checksum
def calc_snils(s):
    logging.info('Calculating SNILS checksum...')
    sum = 0
    sumstr = ""
    for i in range(9):
        sum += int(s[i])*(9-i)
    if sum > 101:
        sum = sum % 101
    if sum < 100:
        sumstr = str(sum)
        if len(sumstr) == 1:
            sumstr = "0" + sumstr
    elif sum == 100 or sum == 101:
        sumstr = "00"
    logging.debug(f'Intermediate sum: {sum}')
    logging.debug(f'Final checksum: {sumstr}')
    return sumstr

# Regular expressions for checking record elements
patterns = {'telephone': "^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$",
            'snils': "^\d{11}$",
            'university': "^.*(?:[Тт]ех|[Уу]нивер|[Аа]кадем|[Ии]нститут|им\.|СПбГУ|МФТИ|МГ(?:Т|)У).*$",
            'academic_degree': "Бакалавр|Кандидат наук|Магистр|Доктор наук|Специалист",
            'worldview': "^.+(?:изм|анство)$",
            'address': "(?:ул\.|Аллея) (?:им[\.\s]|)[^\s]+"}

# Get command line arguments
parser = argp.ArgumentParser(description="Parser for getting paths to the input and output files")
parser.add_argument("-input", type=str, default="42.txt", help="path to the input file")
parser.add_argument("-output", type=str, default="output.txt", help="path to the output file")
args = parser.parse_args()
input_path = args.input
output_path = args.output

# Class for recording
class Entry:
    data: dict
    
    def __init__(self, d: dict) -> None:
        self.data = d.copy()

    def check_telephone(self) -> bool:
        logging.info('Checking telephone number...')
        if re.match(patterns['telephone'], self.data['telephone']):
            logging.info('Telephone number is valid')
            return True
        logging.warning('Telephone number is invalid')
        return False

    def check_weight(self) -> bool:
        if isinstance(self.data['weight'], int):
            if self.data['weight'] in range(40, 200):
                return True
        return False

    def check_snils(self) -> bool:
        s = self.data['snils']
        if re.match(patterns['snils'], s):
            if re.match(calc_snils(s), s[9:11]):
                return True
        return False

    def check_passport_number(self) -> bool:
        if isinstance(self.data['passport_number'], int):
            if self.data['passport_number'] in range(1000000):
                return True
        return False

    def check_university(self) -> bool:
        if re.match(patterns['university'], self.data['university']):
            return True
        return False

    def check_work_experience(self) -> bool:
        if isinstance(self.data['work_experience'], int):
            if self.data['work_experience'] in range(101):
                return True
        return False

    def check_academic_degree(self) -> bool:
        if re.match(patterns['academic_degree'], self.data['academic_degree']):
            return True
        return False

    def check_worldview(self) -> bool:
        if re.match(patterns['worldview'], self.data['worldview']):
            return True
        return False

    def check_address(self) -> bool:
        if re.match(patterns['address'], self.data['address']):
            return True
        return False

class Validator:
    entries: list

    def __init__(self, path: str) -> None:
        logging.info('Loading data from JSON file...')
        logging.debug(f'Path: {path}')
        self.entries = []
        tmp = json.load(open(path, encoding="windows-1251"))
        for i in tmp:
            self.entries.append(Entry(i.copy()))

    def process(self, path: str) -> None:
        logging.info('Validation process started...')
        tmp = []
        for i in tqdm(range(len(self.entries)), desc="Writing valid entries to file", ncols=100):
            if not (False in self.validate(i).values()):
                logging.info(f'Entry {i} is valid')
                tmp.append(self.entries[i].data.copy())
            else:
                logging.warning(f'Entry {i} is invalid')
        logging.info(f'Number of valid entries found: {len(tmp)}')
        json.dump(tmp, open(path, "w", encoding="windows-1251"), ensure_ascii=False, sort_keys=True, indent=4)
        logging.info('Validation process completed')

    def validate(self, index: int) -> dict:
            res = {}
            if not (index in range(len(self.entries))):
                raise Exception("Validation error: index out of range!")
            res['telephone'] = self.entries[index].check_telephone()
            res['weight'] = self.entries[index].check_weight()
            res['snils'] = self.entries[index].check_snils()
            res['passport_number'] = self.entries[index].check_passport_number()
            res['university'] = self.entries[index].check_university()
            res['work_experience'] = self.entries[index].check_work_experience()
            res['academic_degree'] = self.entries[index].check_academic_degree()
            res['worldview'] = self.entries[index].check_worldview()
            res['address'] = self.entries[index].check_address()

            logging.info(f"Validation results for entry at index {index}: {res}")

            return res.copy()

    def count_entries(self, isvalid: bool) -> int:
        count = len(self.entries)
        if isvalid:
            for i in tqdm(range(len(self.entries)), desc="Searching for valid entries", ncols=100):
                if False in self.validate(i).values():
                    count -= 1
        else:
            for i in tqdm(range(len(self.entries)), desc="Searching for invalid entries", ncols=100):
                if not (False in self.validate(i).values()):
                    count -= 1
        return count

    def count_by_error(self, field: str):
        count = 0
        for i in tqdm(range(len(self.entries)), desc=f"Searching by error in field \"{field}\"", ncols=100):
            if self.validate(i)[field] == False:
                count += 1
        return count

if __name__ == "__main__":
    setup_logging()
    val = Validator(input_path)
    logging.info(f"Number of valid entries: {val.count_entries(True)}")
    logging.info(f"Number of invalid entries: {val.count_entries(False)}")
    for i in val.validate(0).keys():
        logging.info(f"Number of entries with error in {i}: {val.count_by_error(i)}")
    val.process(output_path)