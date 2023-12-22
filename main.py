import csv
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("Employees.log")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class Employee:
    employees: List["Employee"] = []

    def __init__(self, first_name: str, last_name: str, age: int, position: str, email: str, phone: str, id: int) -> None:
        '''Конструктор класса Employee'''
        for empl in Employee.employees:
            if id == empl.id:
                logger.error("Failed to create employee")
                raise ValueError("Уже существует сотрудник с таким идентификатором")
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.position = position
        self.email = email
        self.phone = phone
        self.id = id
        Employee.employees.append(self)
        logger.info(f"Employee created: {self}")

    def __str__(self) -> str:
        '''Возвращает строковое представление сотрудника'''
        return (f"{self.first_name} {self.last_name}, Age: {self.age}, "
                f"Position: {self.position}, Email: {self.email},"
                f"Phone: {self.phone}, ID: {self.id}")

    @classmethod
    def print_empl(cls) -> None:
        '''Выводит информацию о всех сотрудниках'''
        if len(cls.employees) > 0:
            for empl in cls.employees:
                print(f"{empl.first_name} {empl.last_name}, Age: {empl.age}, "
                    f"Position: {empl.position}, Email: {empl.email},"
                    f"Phone: {empl.phone}, ID: {empl.id}")
        else:
            logger.error("Failed to print employee list")
            raise ValueError("В компании нет сотрудников")
    
    @classmethod
    def get_employee(cls, employee_id: int) -> Optional["Employee"]:
        '''Находит сотрудника по идентификатору'''
        for employee in cls.employees:
            if employee_id == employee.id:
                logger.info(f"Employee was get: {employee}")
                return employee
        logger.error("Failed to get employee")
        raise ValueError("В компании нет сотрудника с таким идентификатором")

    @classmethod
    def add_employee(cls, empl: Optional["Employee"]) -> None:
        '''Добавляет сотрудника в компанию'''
        for employee in cls.employees:
            if empl.id == employee.id:
                logger.error("Failed to add employee")
                raise ValueError("Уже существует сотрудник с таким идентификатором")
        cls.employees.append(employee)
        logger.info(f"Employee was add: {employee}")

    @classmethod
    def remove_employee(cls, employee_id: int) -> None:
        '''Удаляет сотрудника из компании'''
        for employee in cls.employees:
            if employee_id == employee.id:
                logger.info(f"Employee was remove: {employee}")
                cls.employees.remove(employee)
                return None
        logger.error("Failed to remove employee")
        raise ValueError("В компании нет сотрудника с таким идентификатором")
    
    @classmethod
    def sort_by_first_name(cls) -> None:
        '''Сортирует сотрудников по имени'''
        cls.employees.sort(key=lambda x: x.first_name)
        logger.info(f"Employees were sorted by first name")

    @classmethod
    def sort_by_last_name(cls) -> None:
        '''Сортирует сотрудников по фамилии'''
        cls.employees.sort(key=lambda x: x.last_name)
        logger.info(f"Employees were sorted by last name")

    @classmethod
    def sort_by_age(cls) -> None:
        '''Сортирует сотрудников по возрасту'''
        cls.employees.sort(key=lambda x: x.age)
        logger.info(f"Employees were sorted by age")

    def change_first_name(self, first_name: str) -> None:
        '''Меняет имя сотрудника'''
        self.first_name = first_name
        logger.info(f"Employee's first name has been changed: {first_name}")

    def change_last_name(self, last_name: str) -> None:
        '''Меняет фамилию сотрудника'''
        self.last_name = last_name
        logger.info(f"Employee's last name has been changed: {last_name}")

    def change_age(self, age: int) -> None:
        '''Меняет возраст сотрудника'''
        self.age = age
        logger.info(f"Employee's age has been changed: {age}")

    def change_position(self, position: str) -> None:
        '''Меняет должность сотрудника'''
        self.position = position
        logger.info(f"Employee's position has been changed: {position}")

    def change_email(self, email: str) -> None:
        '''Меняет почту сотрудника'''
        self.email = email
        logger.info(f"Employee's email has been changed: {email}")

    def change_phone(self, phone: str) -> None:
        '''Меняет телефон сотрудника'''
        self.phone = phone
        logger.info(f"Employee's phone has been changed: {phone}")

    @classmethod
    def write_to_csv(cls, filename: str) -> None:
        '''Записывает информацию о сотрудниках в csv файл'''
        try:    
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['first_name', 'last_name', 'age', 'position', 'email', 'phone', 'id']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                writer.writeheader()
                for employee in cls.employees:
                    writer.writerow({'first_name': employee.first_name,
                                    'last_name': employee.last_name,
                                    'age': employee.age,
                                    'position': employee.position,
                                    'email': employee.email,
                                    'phone': employee.phone,
                                    'id': employee.id})
            logger.info(f"Employees written to csv file: {filename}")
        except Exception as e:
            logger.error(f"Error writing to CSV file: {filename} - {e}")

    @classmethod
    def read_from_csv(cls, filename: str) -> None:
        '''Считывает информацию о сотрудниках из csv файла'''
        try:
            with open(filename, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                cls.employees = []
                for row in reader:
                    employee = cls(first_name=row['first_name'],
                                last_name=row['last_name'],
                                age=int(row['age']),
                                position=row['position'],
                                email=row['email'],
                                phone=row['phone'],
                                id=int(row['id']))
            logger.info(f"Employees data uploaded from csv file {filename}")
        except Exception as e:
            logger.error(f"Error reading to CSV file: {filename} - {e}")

if __name__ == "__main__":
    try:
        employee1 = Employee(first_name="John", last_name="Doe", age=30, position="Software Engineer", 
                         email="john@example.com", phone="555-1234", id = 1)
        employee2 = Employee(first_name="Jane", last_name="Smith", age=28, position="Data Scientist", 
                         email="jane@example.com", phone="555-5678", id = 2)
        employee3 = Employee(first_name="Alice", last_name="Johnson", age=35, position="Project Manager", 
                         email="alice@example.com", phone="555-9876", id = 3)
        employee4 = Employee(first_name="Bob", last_name="Williams", age=32, position="UX Designer", 
                         email="bob@example.com", phone="555-8765", id = 4)
        employee5 = Employee(first_name="Eva", last_name="Brown", age=29, position="Software Developer", 
                         email="eva@example.com", phone="555-3456", id = 5)
        employee6 = Employee(first_name="Charlie", last_name="Jones", age=27, position="Data Analyst", 
                         email="charlie@example.com", phone="555-2345", id = 6)
        print(employee1)
        print(employee2)

        employee5.change_age(30)
        employee6.change_phone("555-8800")

        Employee.sort_by_first_name()
        Employee.write_to_csv("sorted_employees.csv")
        Employee.read_from_csv("123.csv")
    except Exception as e:
        print(f"An error occurred: {e}")

