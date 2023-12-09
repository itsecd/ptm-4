import csv


class GymJournal:
    def __init__(self):
        self.clients = []

    def change_name(self, first_name, last_name, new_first_name, new_last_name):
        for client in self.clients:
            if client["first_name"] == first_name and client["last_name"] == last_name:
                client["first_name"] = new_first_name
                client["last_name"] = new_last_name
                return True
        return False

    def change_months(self, first_name, last_name, new_months):
        for client in self.clients:
            if client["first_name"] == first_name and client["last_name"] == last_name:
                client["months"] = new_months
                return True
        return False

    def check_client(self, first_name, last_name):
        for client in self.clients:
            if client["first_name"] == first_name and client["last_name"] == last_name:
                return True
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

    def remove_client(self, first_name, last_name):
        for client in self.clients:
            if client["first_name"] == first_name and client["last_name"] == last_name:
                self.clients.remove(client)
                return True
        return False

    def sort_by_name(self):
        self.clients.sort(key=lambda x: (x["first_name"], x["last_name"]))

    def sort_by_months(self):
        self.clients.sort(key=lambda x: x["months"])

    def read_from_csv(self, file_path):
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.clients.append(row)

    def write_to_csv(self, file_path):
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


try:
    if __name__ == "__main__":
        gym = GymJournal()

        # Пример использования методов
        gym.add_client("John", "Doe", "2022-01-01", "2022-06-30", 6)
        gym.add_client("Jane", "Smith", "2022-02-15", "2022-08-15", 6)

        gym.sort_by_name()
        print("Clients sorted by name:")
        for client in gym.clients:
            print(client)

        gym.sort_by_months()
        print("Clients sorted by months:")
        for client in gym.clients:
            print(client)

        gym.change_name("John", "Doe", "Johnny", "Doe")
        gym.change_months("Jane", "Smith", 12)

        print("Updated clients:")
        for client in gym.clients:
            print(client)

        gym.write_to_csv("clients.csv")

        new_gym = GymJournal()
        new_gym.read_from_csv("clients.csv")

        print("Clients read from csv:")
        for client in new_gym.clients:
            print(client)
except Exception as e:
    print("An error occurred:", e)