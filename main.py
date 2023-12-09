import csv
import logging
from logging.handlers import RotatingFileHandler

# Настройка логирования
logger = logging.getLogger('GymJournalLogger')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('gym_journal.log', maxBytes=5000000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)')
handler.setFormatter(formatter)
logger.addHandler(handler)

class GymJournal:
    def __init__(self):
        self.clients = []
        logger.info('GymJournal instance created')

    def change_name(self, first_name, last_name, new_first_name, new_last_name):
        for client in self.clients:
            if client["first_name"] == first_name and client["last_name"] == last_name:
                client["first_name"] = new_first_name
                client["last_name"] = new_last_name
                logger.info(f'Name changed from {first_name} {last_name} to {new_first_name} {new_last_name}')
                return True
        logger.warning(f'Name change failed for {first_name} {last_name}')
        return False

    def change_months(self, first_name, last_name, new_months):
        for client in self.clients:
            if client["first_name"] == first_name and client["last_name"] == last_name:
                client["months"] = new_months
                logger.info(f'Months changed for {first_name} {last_name} to {new_months}')
                return True
        logger.warning(f'Months change failed for {first_name} {last_name}')
        return False

    def check_client(self, first_name, last_name):
        for client in self.clients:
            if client["first_name"] == first_name and client["last_name"] == last_name:
                logger.info(f'Client found: {first_name} {last_name}')
                return True
        logger.info(f'Client not found: {first_name} {last_name}')
        return False

    def add_client(self, first_name, last_name, purchase_date, end_date, months):
        self.clients.append(
            {
                "first_name": first_name,
                "last_name": last_name,
                "purchase_date": purchase_date,
                "end_date": end_date,
                "months": months,
            }
        )
        logger.info(f'Client added: {first_name} {last_name}')

    def remove_client(self, first_name, last_name):
        for client in self.clients:
            if client["first_name"] == first_name and client["last_name"] == last_name:
                self.clients.remove(client)
                logger.info(f'Client removed: {first_name} {last_name}')
                return True
        logger.warning(f'Removal failed for {first_name} {last_name}')
        return False

    def sort_by_name(self):
        self.clients.sort(key=lambda x: (x["first_name"], x["last_name"]))
        logger.info('Clients sorted by name')

    def sort_by_months(self):
        self.clients.sort(key=lambda x: x["months"])
        logger.info('Clients sorted by months')

    def read_from_csv(self, file_path):
        try:
            with open(file_path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.clients.append(row)
            logger.info(f'Clients read from CSV file: {file_path}')
        except Exception as e:
            logger.error(f'Error reading from CSV file: {file_path} - {e}')

    def write_to_csv(self, file_path):
        try:
            with open(file_path, "w", newline="") as file:
                fieldnames = [
                    "first_name",
                    "last_name",
                    "purchase_date",
                    "end_date",
                    "months",
                ]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for client in self.clients:
                    writer.writerow(client)
            logger.info(f'Clients written to CSV file: {file_path}')
        except Exception as e:
            logger.error(f'Error writing to CSV file: {file_path} - {e}')

if __name__ == "__main__":
    gym = GymJournal()

    # Пример использования методов
    gym.add_client("John", "Doe", "2022-01-01", "2022-06-30", 6)
    gym.add_client("Jane", "Smith", "2022-02-15", "2022-08-15", 6)

    gym.sort_by_name()
    logger.info("Clients sorted by name:")
    for client in gym.clients:
        logger.info(client)

    gym.sort_by_months()
    logger.info("Clients sorted by months:")
    for client in gym.clients:
        logger.info(client)

    gym.change_name("John", "Doe", "Johnny", "Doe")
    gym.change_months("Jane", "Smith", 12)

    logger.info("Updated clients:")
    for client in gym.clients:
        logger.info(client)

    gym.write_to_csv("clients.csv")

    new_gym = GymJournal()
    new_gym.read_from_csv("clients.csv")

    logger.info("Clients read from csv:")
    for client in new_gym.clients:
        logger.info(client)
