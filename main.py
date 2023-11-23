import argparse as argp
import json
import re
from tqdm import tqdm

# вычисление контрольной суммы снилса и выдача в виде строки для сравнения


def calc_snils(s):
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
    return sumstr


# регулярные выражения для проверки элементов записи
patterns = {'telephone': "^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$",
            'snils': "^\d{11}$",
            'university': "^.*(?:[Тт]ех|[Уу]нивер|[Аа]кадем|[Ии]нститут|им\.|СПбГУ|МФТИ|МГ(?:Т|)У).*$",
            'academic_degree': "Бакалавр|Кандидат наук|Магистр|Доктор наук|Специалист",
            'worldview': "^.+(?:изм|анство)$",
            'address': "(?:ул\.|Аллея) (?:им[\.\s]|)[^\s]+ \d+"}


# получение аргументов командной строки
parser = argp.ArgumentParser(
    description="Парсер для получения путей к входному и выходному файлу")
parser.add_argument("-input", type=str, default="42.txt",
                    help="путь ко входному файлу")
parser.add_argument("-output", type=str, default="output.txt",
                    help="путь ко выходному файлу")
args = parser.parse_args()
# пути ко входному и выходному файлам
input_path = args.input
output_path = args.output


# класс записи
class Entry:
    '''
    Объект класса Entry репрезентует запись о научном сотруднике.

    Он нужен для хранения полей записи, а также их валидации.

    Attributes
    ----------
        data : dict
            Словарь, хранящий поля записи в виде "название поля": значение.
    '''
    data: dict

    def __init__(self, d: dict) -> None:
        '''
        Инициализирует экземпляр класса записи.

        Parameters
        ----------
            d : dict
                Копия списка с полями записи.
        '''
        self.data = d.copy()

    def check_telephone(self) -> bool:
        '''
        Выполняет валидацию телефонного номера.

        Returns
        -------
            bool:
                Булевый результат проверки на корректность.
        '''
        if re.match(patterns['telephone'], self.data['telephone']):
            return True
        return False

    def check_weight(self) -> bool:
        '''
        Выполняет валидацию веса.

        Returns
        -------
            bool:
                Булевый результат проверки на корректность.
        '''
        if isinstance(self.data['weight'], int):
            if self.data['weight'] in range(40, 200):
                return True
        return False

    def check_snils(self) -> bool:
        '''
        Выполняет валидацию номера СНИЛС.

        Returns
        -------
            bool:
                Булевый результат проверки на корректность.
        '''
        s = self.data['snils']
        if re.match(patterns['snils'], s):
            if re.match(calc_snils(s), s[9:11]):
                return True
        return False

    def check_passport_number(self) -> bool:
        '''
        Выполняет валидацию номера паспорта.

        Returns
        -------
            bool:
                Булевый результат проверки на корректность.
        '''
        if isinstance(self.data['passport_number'], int):
            if self.data['passport_number'] in range(1000000):
                return True
        return False

    def check_university(self) -> bool:
        '''
        Выполняет валидацию названия вуза.

        Returns
        -------
            bool:
                Булевый результат проверки на корректность.
        '''
        if re.match(patterns['university'], self.data['university']):
            return True
        return False

    def check_work_experience(self) -> bool:
        '''
        Выполняет валидацию стажа работы.

        Returns
        -------
            bool:
                Булевый результат проверки на корректность.
        '''
        if isinstance(self.data['work_experience'], int):
            if self.data['work_experience'] in range(101):
                return True
        return False

    def check_academic_degree(self) -> bool:
        '''
        Выполняет валидацию ученой степени.

        Returns
        -------
            bool:
                Булевый результат проверки на корректность.
        '''
        if re.match(patterns['academic_degree'], self.data['academic_degree']):
            return True
        return False

    def check_worldview(self) -> bool:
        '''
        Выполняет валидацию названия мировоззрения.

        Returns
        -------
            bool:
                Булевый результат проверки на корректность.
        '''
        if re.match(patterns['worldview'], self.data['worldview']):
            return True
        return False

    def check_address(self) -> bool:
        '''
        Выполняет валидацию адреса проживания.

        Returns
        -------
            bool:
                Булевый результат проверки на корректность.
        '''
        if re.match(patterns['address'], self.data['address']):
            return True
        return False


class Validator:
    '''
    Объект класса Validator репрезентует валидатор записей научных сотрудников.

    Он нужен для валидации записей и вывода статистики.

    Attributes
    ----------
        entries : list
            Список записей.
    '''
    entries: list

    def __init__(self, path: str) -> None:
        '''
        Инициализирует экземпляр класса валидатора.

        Считывает данные формата json из текстового файла.

        Parameters
        ----------
            path : str
                Путь к файлу с данными.
        '''
        self.entries = []
        tmp = json.load(open(path, encoding="windows-1251"))
        for i in tmp:
            self.entries.append(Entry(i.copy()))

    def process(self, path: str) -> None:
        '''
        Выполняет запись корректных записей в файл.

        Parameters
        ----------
            path : str
                Путь к файлу вывода.
        '''
        tmp = []
        for i in tqdm(range(len(self.entries)), desc="Запись корректных записей в файл", ncols=100):
            if not (False in self.validate(i).values()):
                tmp.append(self.entries[i].data.copy())
        json.dump(tmp, open(path, "w", encoding="windows-1251"),
                  ensure_ascii=False, sort_keys=True, indent=4)

    def validate(self, index: int) -> dict:
        '''
        Выполняет валидацию записи по ее номеру.

        Returns
        -------
            dict:
                Словарь, где каждому полю присвоено логическое значение,
                означающее, корректно это поле записи, или нет.
        '''
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
        return res.copy()

    def count_entries(self, isvalid: bool) -> int:
        '''
        Выполняет поиск корректных/некорректных записей.

        Parameters
        ----------
            isvalid : bool
                Флаг, обозначающий, будут ли искомые записи корректными.

        Returns
        -------
            int:
                Количество корректных/некорректных записей.
        '''
        count = len(self.entries)
        if isvalid:
            for i in tqdm(range(len(self.entries)), desc="Поиск корректных записей", ncols=100):
                if False in self.validate(i).values():
                    count -= 1
        else:
            for i in tqdm(range(len(self.entries)), desc="Поиск некорректных записей", ncols=100):
                if not (False in self.validate(i).values()):
                    count -= 1
        return count

    def count_by_error(self, field: str):
        count = 0
        for i in tqdm(range(len(self.entries)), desc="Поиск по ошибке в поле \""+field+"\"", ncols=100):
            if self.validate(i)[field] == False:
                count += 1
        return count


val = Validator(input_path)
print(val.count_entries(True), "записей найдено!")
print(val.count_entries(False), "записей найдено!")
for i in val.validate(0).keys():
    print(val.count_by_error(i), "записей найдено!")
val.process(output_path)