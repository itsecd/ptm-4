import csv
from datetime import datetime

class VisitJournal:
    def __init__(self):
        self.clients = []

    def change_last_name(self, old_last_name, new_last_name):
        for client in self.clients:
            if client['last_name'] == old_last_name:
                client['last_name'] = new_last_name

    def change_car_brand(self, last_name, new_car_brand):
        for client in self.clients:
            if client['last_name'] == last_name:
                client['car_brand'] = new_car_brand

    def change_days_parked(self, last_name, new_days_parked):
        for client in self.clients:
            if client['last_name'] == last_name:
                client['days_parked'] = new_days_parked

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
        self.clients = [client for client in self.clients if not (client['last_name'] == last_name and client['car_brand'] == car_brand)]

    def sort_by_last_name(self):
        self.clients.sort(key=lambda client: client['last_name'])

    def sort_by_days_parked(self):
        self.clients.sort(key=lambda client: client['days_parked'] if client['days_parked'] is not None else float('inf'))

    def read_from_file(self, file_name):
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

    def write_to_file(self, file_name):
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

if __name__ == "__main__":
    try:
        visit = VisitJournal()
        visit.add_client("Ivanov", "BMW", datetime.strptime("2023-11-01", '%Y-%m-%d'))
        visit.add_client("Petrov", "Lada", datetime.strptime("2023-12-15", '%Y-%m-%d'))
        visit.sort_by_last_name()
        print("Clients sorted by last_name:")
        for client in visit.clients:
            print(client)
        visit.sort_by_days_parked()
        print("Clients sorted by days:")
        for client in visit.clients:
            print(client)
        visit.change_last_name("Ivanov", "Lavruk")
        visit.change_days_parked("Petrov", 12)
        print("Updated clients:")
        for client in visit.clients:
            print(client)
        visit.write_to_file("journal.csv")
        
        new_visit = VisitJournal()
        new_visit.read_from_file("journal.csv")
        print("Clients read from csv:")
        for client in new_visit.clients:
            print(client)
    except Exception as e:
        print("An error occurred:", e)