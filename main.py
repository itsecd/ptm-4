import logging
import json

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.owned_books = []

    def __str__(self):
        return f"{self.name}, Возраст: {self.age}"

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.owner = None

    def __str__(self):
        if self.owner:
            return f"{self.title} (Автор: {self.author}, Владелец: {self.owner.name})"
        else:
            return f"{self.title} (Автор: {self.author}, Владелец: Нет)"

class Library:
    def __init__(self) -> None:
        self.people = []
        self.books = []
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler('library_log.txt')
        #file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        #logger.addHandler(file_handler)
        return logger

    def add_person(self, person: Person) -> None:
        self.people.append(person)

    def remove_person(self, person: Person) -> None:
        if person in self.people:
            self.people.remove(person)
        else:
            print(f"Попытка удалить несуществующую персону: {person}")

    def add_book(self, book: Book) -> None:
        self.books.append(book)

    def remove_book(self, book: Book) -> None:
        if book in self.books:
            self.books.remove(book)
        else:
            print(f"Попытка удалить несуществующую книгу: {book}")

    def lend_book(self, book: Book, person: Person) -> None:
        if book in self.books and person in self.people:
            book.owner = person
            person.owned_books.append(book)
        else:
            print(f"Невозможно выдать книгу {book} в аренду {person}")

    def display_people(self) -> None:
        self.logger.info("Вывод информации о людях:")
        for person in self.people:
            print(person)

    def display_books(self) -> None:
        for book in self.books:
            print(book)

    def save_to_txt(self, filename: str = 'library.txt') -> None:
        data = {
            'people': [str(person) for person in self.people],
            'books': [str(book) for book in self.books]
        }
        try:
            with open(filename, 'w') as txtfile:
                json.dump(data, txtfile, indent=2)
        except Exception as e:
            print(f"Ошибка при сохранении данных о библиотеке в файл {filename}: {str(e)}")

    def load_from_txt(self, filename: str = 'library.txt') -> None:
        try:
            with open(filename, 'r') as txtfile:
                data = json.load(txtfile)
                for person_str in data['people']:
                    name, age = [item.strip() for item in person_str.split(',')]
                    self.add_person(Person(name, int(age)))
                for book_str in data['books']:
                    title_author, owner = [item.strip() for item in book_str.split(' (Владелец: ')]
                    title, author = [item.strip() for item in title_author.split(' (Автор: ')]
                    owner = owner[:-1]  # Удаляем последний символ ')' из owner
                    book = Book(title, author)
                    self.add_book(book)
                    if owner != "Нет":
                        owner_person = next((person for person in self.people if person.name == owner), None)
                        if owner_person:
                            self.lend_book(book, owner_person)
            print(f"Данные о библиотеке загружены из файла: {filename}")
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")
        except Exception as e:
            print(f"Ошибка при загрузке данных о библиотеке из файла {filename}: {str(e)}")

if __name__ == "__main__":
    try:
        library = Library()

        person1 = Person("Alice", 25)
        person2 = Person("Bob", 30)

        book1 = Book("The Great Gatsby", "F. Scott Fitzgerald")
        book2 = Book("To Kill a Mockingbird", "Harper Lee")

        library.add_person(person1)
        library.add_person(person2)
        library.add_book(book1)
        library.add_book(book2)

        library.lend_book(book1, person1)
        library.lend_book(book2, person2)

        library.display_people()
        library.display_books()

        library.save_to_txt()
        library.load_from_txt()

        library.display_people()
        library.display_books()

    except Exception as e:
        print("Произошла ошибка")
