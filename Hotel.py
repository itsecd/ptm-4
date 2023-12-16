import csv
import logging
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler('hotel.log')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

class Client:
    def __init__(self, first_name, last_name, check_in_date, check_out_date, room_class):
        self.first_name = first_name
        self.last_name = last_name
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.room_class = room_class

class Hotel:
    def __init__(self, csv_filename):
        self.clients = []
        self.csv_filename = csv_filename

    def add_client(self, client):
        self.clients.append(client)
        self.append_client_to_csv(client)
        logger.info(f'Client {client.first_name} {client.last_name} added')

    def remove_client(self, first_name, last_name):
        self.clients = [client for client in self.clients if client.first_name != first_name or client.last_name != last_name]
        logger.info(f'Client {first_name} {last_name} removed')

    def client_exists(self, first_name, last_name):
        exists = any(client.first_name == first_name and client.last_name == last_name for client in self.clients)
        logger.info(f'Client {first_name} {last_name} exists: {exists}')
        return exists

    def count_clients(self):
        with open(self.csv_filename, 'r') as file:
            reader = csv.reader(file)
            next(reader) 
            count = sum(1 for row in reader)
            logger.info(f'Counted clients: {count}')
            return count

    def change_name(self, old_first_name, old_last_name, new_first_name, new_last_name):
        for client in self.clients:
            if client.first_name == old_first_name and client.last_name == old_last_name:
                client.first_name = new_first_name
                client.last_name = new_last_name
                logger.info(f'Changed name for client {old_first_name} {old_last_name} to {new_first_name} {new_last_name}')

    def extend_stay(self, first_name, last_name, extra_days):
        for client in self.clients:
            if client.first_name == first_name and client.last_name == last_name:
                client.check_out_date += timedelta(days=extra_days)
                logger.info(f'Extended stay for client {first_name} {last_name} by {extra_days} days')

    def change_room_class(self, first_name, last_name, new_room_class):
        for client in self.clients:
            if client.first_name == first_name and client.last_name == last_name:
                client.room_class = new_room_class
                logger.info(f'Changed room class for client {first_name} {last_name} to {new_room_class}')

    def read_from_csv(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                first_name, last_name, check_in_date, check_out_date, room_class = row
                check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d')
                check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d')
                client = Client(first_name, last_name, check_in_date, check_out_date, room_class)
                self.add_client(client)
                logger.info(f'Read client {first_name} {last_name} from CSV')

    def write_to_csv(self, filename):
        with open(filename, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['First Name', 'Last Name', 'Check-in Date', 'Check-out Date', 'Room Class'])
            for client in self.clients:
                row = [client.first_name, client.last_name, client.check_in_date.strftime('%Y-%m-%d'), client.check_out_date.strftime('%Y-%m-%d'), client.room_class]
                writer.writerow(row)
                logger.info(f'Wrote client {client.first_name} {client.last_name} to CSV')

    def append_client_to_csv(self, client):
        with open(self.csv_filename, 'a', newline='') as file:
            writer = csv.writer(file)
            row = [client.first_name, client.last_name, client.check_in_date.strftime('%Y-%m-%d'), client.check_out_date.strftime('%Y-%m-%d'), client.room_class]
            writer.writerow(row)
            logger.info(f'Appended client {client.first_name} {client.last_name} to CSV')


if __name__ == "__main__":
    try:
        
        logger.info("Starting the program")
        hotel = Hotel("clients.csv")
        
        logger.info("Created hotel with clients.csv")

        client1 = Client("Иван", "Иванов", datetime(2023, 12, 1), datetime(2023, 12, 10), "Стандарт")
        client2 = Client("Петр", "Петров", datetime(2023, 12, 5), datetime(2023, 12, 15), "Люкс")
        client3 = Client("Василий", "Гришков", datetime(2023, 12, 1), datetime(2023, 12, 10), "Стандарт")
        client4 = Client("Николай", "Петрин", datetime(2023, 12, 5), datetime(2023, 12, 15), "Люкс")

        hotel.add_client(client1)
        hotel.add_client(client2)
        hotel.add_client(client3)
        hotel.add_client(client4)

        hotel.change_name("Иван", "Иванов", "Алексей", "Иванов")

        hotel.extend_stay("Алексей", "Иванов", 5)

        hotel.change_room_class("Петр", "Петров", "Президентский")

        print(hotel.client_exists("Алексей", "Иванов"))

        hotel.remove_client("Петр", "Петров")

        print(hotel.count_clients())

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        logger.error(f"An error occurred: {e}")