import logging
import json


class Person:
    def __init__(self, name: str, age: int) -> None:
        """
        Инициализация объекта Person.
        :param name: Имя персоны.
        :param age: Возраст персоны.
        """
        self.name = name
        self.age = age
        self.owned_books = []

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта Person.
        :return: Строковое представление объекта Person.
        """
        return f"{self.name}, Age: {self.age}"


class Book:
    def __init__(self, title: str, author: str) -> None:
        """
        Инициализация объекта Book.
        :param title: Название книги.
        :param author: Автор книги.
        """
        self.title = title
        self.author = author
        self.owner = None

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта Book.
        :return: Строковое представление объекта Book.
        """
        if self.owner:
            return f"{self.title} (Author: {self.author}, Owner: {self.owner.name})"
        else:
            return f"{self.title} (Author: {self.author}, Owner: No)"


class Library:
    def __init__(self) -> None:
        """
        Инициализация объекта Library.
        """
        self.people = []
        self.books = []
        self.logger = self.setup_logger()

    @staticmethod
    def setup_logger():
        """
        Настройка логгера.
        :return: Объект логгера.
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler('library_log.txt')
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def add_person(self, person: Person) -> None:
        """
        Добавляет персону в библиотеку.
        :param person: Объект Person.
        :return: None
        """
        self.people.append(person)
        self.logger.info(f"Person added: {person}")

    def remove_person(self, person: Person) -> None:
        """
        Удаляет персону из библиотеки.
        :param person: Объект Person.
        :return: None
        """
        if person in self.people:
            self.people.remove(person)
            self.logger.info(f"The person has been deleted: {person}")
        else:
            self.logger.warning(f"Attempt to delete a non-existent person: {person}")

    def add_book(self, book: Book) -> None:
        """
        Добавляет книгу в библиотеку.
        :param book: Объект Book.
        :return: None
        """
        self.books.append(book)
        self.logger.info(f"Book added: {book}")

    def remove_book(self, book: Book) -> None:
        """
        Удаляет книгу из библиотеки.
        :param book: Объект Book.
        :return: None
        """
        if book in self.books:
            self.books.remove(book)
            self.logger.info(f"Book deleted: {book}")
        else:
            self.logger.warning(f"Attempt to delete a non-existent book: {book}")

    def lend_book(self, book: Book, person: Person) -> None:
        """
        Выдает книгу в аренду персоне.
        :param book: Объект Book.
        :param person: Объект Person.
        :return: None
        """
        if book in self.books and person in self.people:
            book.owner = person
            person.owned_books.append(book)
            self.logger.info(f"{person} I rented a book: {book}")
        else:
            self.logger.warning(f"It is impossible to issue a book {book} for rent {person}")

    def display_people(self) -> None:
        """
        Выводит информацию о людях в библиотеке.
        :return: None
        """
        self.logger.info("Output of information about people:")
        for person in self.people:
            self.logger.debug(person)

    def display_books(self) -> None:
        """
        Выводит информацию о книгах в библиотеке.
        :return: None
        """
        self.logger.info("Output of information about books:")
        for book in self.books:
            self.logger.debug(book)

    def save_to_txt(self, filename: str = 'library.txt') -> None:
        """
        Сохраняет информацию о библиотеке в текстовый файл.
        :param filename: Название файла.
        :return: None
        """
        data = {
            'people': [str(person) for person in self.people],
            'books': [str(book) for book in self.books]
        }
        try:
            with open(filename, 'w') as txtfile:
                json.dump(data, txtfile, indent=2)
            self.logger.info(f"The library data is saved to a file: {filename}")
        except Exception as e:
            self.logger.warning(f"Error when saving library data to a file {filename}: {str(e)}")

    def load_from_txt(self, filename: str = 'library.txt') -> None:
        """
        Загружает информацию о библиотеке из текстового файла.
        :param filename: Название файла.
        :return: None
        """
        try:
            with open(filename, 'r') as txtfile:
                data = json.load(txtfile)
                for person_str in data['people']:
                    name, age = [item.strip() for item in person_str.split(',')]
                    self.add_person(Person(name, int(age)))
                for book_str in data['books']:
                    title_author, owner = [item.strip() for item in book_str.split(' (Owner: ')]
                    title, author = [item.strip() for item in title_author.split(' (Author: ')]
                    owner = owner[:-1]
                    book = Book(title, author)
                    self.add_book(book)
                    if owner != "No":
                        owner_person = next((person for person in self.people if person.name == owner), None)
                        if owner_person:
                            self.lend_book(book, owner_person)
            self.logger.info(f"The library data is loaded from a file: {filename}")
        except FileNotFoundError:
            self.logger.warning(f"File {filename} not found.")
        except Exception as e:
            self.logger.warning(f"Error loading library data from a file {filename}: {str(e)}")


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
    except ValueError as e:
        logging.exception("An error has occurred", exc_info=True)
