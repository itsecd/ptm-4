import csv
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

class VisitJournal:
    def __init__(self):
        self.clients = []

         # Configure logging
        logging.basicConfig(filename='visit_journal.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)


    def change_last_name(self, old_last_name, new_last_name):
        for client in self.clients:
            if client['last_name'] == old_last_name:
                client['last_name'] = new_last_name
                self.logger.info(f'Changed last name for {old_last_name} to {new_last_name}')

    def change_car_brand(self, last_name, new_car_brand):
        for client in self.clients:
            if client['last_name'] == last_name:
                client['car_brand'] = new_car_brand
                self.logger.info(f'Changed car brand for {last_name} to {new_car_brand}')

    def change_days_parked(self, last_name, new_days_parked):
        for client in self.clients:
            if client['last_name'] == last_name:
                client['days_parked'] = new_days_parked
                self.logger.info(f'Changed days parked for {last_name} to {new_days_parked}')

    def check_client_existence(self, last_name, car_brand):
        for client in self.clients:
            if client['last_name'] == last_name and client['car_brand'] == car_brand:
                return True
        return False

    def add_client(self, last_name, car_brand, entry_date):
        # Assuming entry_date is of type datetime
        self.clients.append({
            'last_name': last_name,
            'car_brand': car_brand,
            'entry_date': entry_date,
            'exit_from_parking': None,
            'days_parked': None
        })

    def remove_client(self, last_name, car_brand):
        logger = logging.getLogger(__name__)
        logger.info(f'Removing client with last name {last_name} and car brand {car_brand}')
        self.clients = [client for client in self.clients if not (client['last_name'] == last_name and client['car_brand'] == car_brand)]
        logger.info('Client removed successfully')

    def sort_by_last_name(self):
        logger = logging.getLogger(__name__)
        logger.info('Sorting clients by last name')
        self.clients.sort(key=lambda client: client['last_name'])
        logger.info('Clients sorted by last name')

    def sort_by_days_parked(self):
        logger = logging.getLogger(__name__)
        logger.info('Sorting clients by days parked')
        self.clients.sort(key=lambda client: client['days_parked'] if client['days_parked'] is not None else float('inf'))
        logger.info('Clients sorted by days parked')

    def read_from_file(self, file_name):
        logger = logging.getLogger(__name__)
        logger.info(f'Reading clients from file {file_name}')
        with open(file_name, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.clients.append({
                    'last_name': row['last_name'],
                    'car_brand': row['car_brand'],
                    'entry_date': datetime.strptime(row['entry_date'], '%Y-%m-%d'),
                    'exit_from_parking': datetime.strptime(row['exit_from_parking'], '%Y-%m-%d') if row['exit_from_parking'] else None,
                    'days_parked': int(row['days_parked']) if row['days_parked'] else None
                })
        logger.info('Clients read from file')

    def write_to_file(self, file_name):
        logger = logging.getLogger(__name__)
        logger.info(f'Writing clients to file {file_name}')
        with open(file_name, 'w', newline='') as csvfile:
            fieldnames = ['last_name', 'car_brand', 'entry_date', 'exit_from_parking', 'days_parked']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for client in self.clients:
                writer.writerow({
                    'last_name': client['last_name'],
                    'car_brand': client['car_brand'],
                    'entry_date': client['entry_date'].strftime('%Y-%m-%d'),
                    'exit_from_parking': client['exit_from_parking'].strftime('%Y-%m-%d') if client['exit_from_parking'] else '',
                    'days_parked': client['days_parked'] if client['days_parked'] else ''
                })
        logger.info('Clients written to file')


if __name__ == "__main__":
    try:
        # Configure logging
        logging.basicConfig(filename='visit_journal.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)

        logger.info('Starting the main block')

        visit = VisitJournal()
        visit.add_client("Ivanov", "BMW", datetime.strptime("2023-11-01", '%Y-%m-%d'))
        visit.add_client("Petrov", "Lada", datetime.strptime("2023-12-15", '%Y-%m-%d'))
        visit.sort_by_last_name()
        logger.info('Clients sorted by last name')
        for client in visit.clients:
            logger.info(f'Client: {client}')
        
        visit.sort_by_days_parked()
        logger.info('Clients sorted by days parked')
        for client in visit.clients:
            logger.info(f'Client: {client}')
        
        visit.change_last_name("Ivanov", "Lavruk")
        logger.info('Changed last name for Ivanov to Lavruk')
        
        visit.change_days_parked("Petrov", 12)
        logger.info('Changed days parked for Petrov to 12')
        
        logger.info('Updated clients')
        for client in visit.clients:
            logger.info(f'Client: {client}')
        
        visit.write_to_file("journal.csv")
        
        new_visit = VisitJournal()
        new_visit.read_from_file("journal.csv")
        
        logger.info('Clients read from csv')
        for client in new_visit.clients:
            logger.info(f'Client: {client}')

    except Exception as e:
        logger.error(f'An error occurred: {e}')