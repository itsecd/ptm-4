import logging
from datetime import datetime, timedelta
from collections import defaultdict

class VisitorTracker:
    def __init__(self):
        self.visitors = defaultdict(list)
        self.user_count = 0
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger("VisitorTracker")
        logger.setLevel(logging.DEBUG)

        # Создание файла лога
        file_handler = logging.FileHandler("visitor_tracker.log")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        return logger

    def log_event(self, message):
        self.logger.info(message)

    def register_user(self):
        self.user_count += 1
        user_id = f"Person{self.user_count}"
        self.log_event(f"User {user_id} registered.")
        return user_id

    def enter_building(self, person_id):
        entry_time = datetime.now()
        self.visitors[person_id].append({"entry_time": entry_time, "exit_time": None})
        self.log_event(f"User {person_id} entered the building at {entry_time}.")

    def exit_building(self, person_id):
        exit_time = datetime.now()
        if person_id in self.visitors and self.visitors[person_id][-1]["exit_time"] is None:
            self.visitors[person_id][-1]["exit_time"] = exit_time
            self.log_event(f"User {person_id} exited the building at {exit_time}.")

    def calculate_duration(self, person_id):
        total_duration = timedelta()
        if person_id in self.visitors:
            for visit in self.visitors[person_id]:
                if visit["exit_time"] is not None:
                    total_duration += visit["exit_time"] - visit["entry_time"]
        return total_duration

    def calculate_frequency(self, person_id):
        return len(self.visitors.get(person_id, []))

    def attendance_info(self):
        for person_id, visits in self.visitors.items():
            self.log_event(f"Attendance info for user {person_id}:")
            for visit in visits:
                entry_time = visit["entry_time"].strftime("%Y-%m-%d %H:%M:%S")
                exit_time = visit["exit_time"].strftime("%Y-%m-%d %H:%M:%S") if visit["exit_time"] else "N/A"
                self.log_event(f"  Entry: {entry_time}, Exit: {exit_time}")
            self.log_event(f"  Total Duration: {self.calculate_duration(person_id)}")
            self.log_event(f"  Visit Frequency: {self.calculate_frequency(person_id)}\n")

    def overall_statistics(self):
        total_duration = timedelta()
        total_visits = 0

        for person_id, visits in self.visitors.items():
            total_visits += len(visits)
            total_duration += self.calculate_duration(person_id)

        self.log_event("Overall Statistics:")
        self.log_event(f"  Total Visits: {total_visits}")
        self.log_event(f"  Total Duration: {total_duration}")

    def check_warning(self, person_id, max_duration):
        current_duration = self.calculate_duration(person_id)
        if current_duration < max_duration:
            self.log_event(f"Warning: User {person_id} is inside for less than {max_duration}.")

# Консольное меню
def main():
    tracker = VisitorTracker()

    while True:
        print("\nMenu:")
        print("1. Add User")
        print("2. List All Users")
        print("3. Enter Building")
        print("4. Exit Building")
        print("5. View Attendance Info")
        print("6. View Overall Statistics")
        print("7. Check Warning")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            user_id = tracker.register_user()
            print(f"User {user_id} added successfully.")

        elif choice == "2":
            print("List of All Users:")
            for user_id in tracker.visitors.keys():
                print(user_id)

        elif choice == "3":
            user_id = input("Enter user ID: ")
            tracker.enter_building(user_id)
            print(f"User {user_id} entered the building.")

        elif choice == "4":
            user_id = input("Enter user ID: ")
            tracker.exit_building(user_id)
            print(f"User {user_id} exited the building.")

        elif choice == "5":
            tracker.attendance_info()

        elif choice == "6":
            tracker.overall_statistics()

        elif choice == "7":
            user_id = input("Enter user ID: ")
            max_duration = timedelta(minutes=int(input("Enter maximum allowed duration (in minutes): ")))
            tracker.check_warning(user_id, max_duration)

        elif choice == "0":
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
