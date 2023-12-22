import csv


class Employee:
    employees = []

    def __init__(self, first_name, last_name, age, position, email, phone, id):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.position = position
        self.email = email
        self.phone = phone
        self.id = id
        Employee.employees.append(self)

    def __str__(self):
        return (f"{self.first_name} {self.last_name}, Age: {self.age}, "
                f"Position: {self.position}, Email: {self.email},"
                f"Phone: {self.phone}, ID: {self.id}")

    @classmethod
    def print_empl(cls):
        for empl in cls.employees:
            print(f"{empl.first_name} {empl.last_name}, Age: {empl.age}, "
                  f"Position: {empl.position}, Email: {empl.email},"
                  f"Phone: {empl.phone}, ID: {empl.id}")
    
    @classmethod
    def get_employee(cls, employee_id):
        for employee in cls.employees:
            if employee_id == employee.id:
                return employee

    @classmethod
    def add_employee(cls, empl):
        for employee in cls.employees:
            if empl.id == employee.id:
                return None
        cls.employees.append(employee)

    @classmethod
    def remove_employee(cls, employee_id):
        for employee in cls.employees:
            if employee_id == employee.id:
                cls.employees.remove(employee)
                return None
    
    @classmethod
    def sort_by_first_name(cls):
        cls.employees.sort(key=lambda x: x.first_name)

    @classmethod
    def sort_by_last_name(cls):
        cls.employees.sort(key=lambda x: x.last_name)

    @classmethod
    def sort_by_age(cls):
        cls.employees.sort(key=lambda x: x.age)

    def change_first_name(self, first_name):
        self.first_name = first_name

    def change_last_name(self, last_name):
        self.last_name = last_name

    def change_age(self, age):
        if (age > self.age):
            self.age = age

    def change_position(self, position):
        self.position = position

    def change_email(self, email):
        self.email = email

    def change_phone(self, phone):
        self.phone = phone

    @classmethod
    def write_to_csv(cls, filename):
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

    @classmethod
    def read_from_csv(cls, filename):
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


if __name__ == "__main__":
    employee1 = Employee(first_name="John", last_name="Doe", age=30, position="Software Engineer", email="john@example.com", phone="555-1234", id = 1)
    employee2 = Employee(first_name="Jane", last_name="Smith", age=28, position="Data Scientist", email="jane@example.com", phone="555-5678", id = 2)
    employee3 = Employee(first_name="Alice", last_name="Johnson", age=35, position="Project Manager", email="alice@example.com", phone="555-9876", id = 3)
    employee4 = Employee(first_name="Bob", last_name="Williams", age=32, position="UX Designer", email="bob@example.com", phone="555-8765", id = 4)
    employee5 = Employee(first_name="Eva", last_name="Brown", age=29, position="Software Developer", email="eva@example.com", phone="555-3456", id = 5)
    employee6 = Employee(first_name="Charlie", last_name="Jones", age=27, position="Data Analyst", email="charlie@example.com", phone="555-2345", id = 6)
    Employee.print_empl()
