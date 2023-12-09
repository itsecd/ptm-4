import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta
from loguru import logger

logger.add("music_subscription.log", format="{time} {level} {message}", level="DEBUG")


class MusicSubscription:
    def __init__(self):
        self.users = []
        logger.info("MusicSubscription object created")

    def add_user(self, name, surname, subscription_start, subscription_end, months_subscribed):
        self.users.append({
            "name": name,
            "surname": surname,
            "subscription_start": datetime.strptime(subscription_start, "%d-%m-%Y"),
            "subscription_end": datetime.strptime(subscription_end, "%d-%m-%Y"),
            "months_subscribed": months_subscribed
        })
        logger.debug(f"User {name} {surname} added to the subscription list")

    def remove_user(self, name, surname):
        self.users = [user for user in self.users if user["name"] != name or user["surname"] != surname]
        logger.debug(f"User {name} {surname} removed from the subscription list")

    def update_user_name(self, old_name, new_name):
        for user in self.users:
            if user["name"] == old_name:
                user["name"] = new_name
                logger.debug(f"User {old_name} changed name to {new_name}")

    def update_user_surname(self, old_surname, new_surname):
        for user in self.users:
            if user["surname"] == old_surname:
                user["surname"] = new_surname
                logger.debug(f"User {old_surname} changed surname to {new_surname}")

    def update_subscription_months(self, name, surname, new_months):
        for user in self.users:
            if user["name"] == name and user["surname"] == surname:
                user["months_subscribed"] = new_months
                logger.debug(f"User {name} {surname} updated subscription months to {new_months}")

    def check_user_exists(self, name, surname):
        exists = any(user["name"] == name and user["surname"] == surname for user in self.users)
        logger.debug(f"Checking if user {name} {surname} exists: {exists}")
        return exists

    def sort_users_by_name(self):
        self.users.sort(key=lambda x: x["name"])
        logger.debug("Users sorted by name")

    def sort_users_by_subscription_months(self):
        self.users.sort(key=lambda x: x["months_subscribed"])
        logger.debug("Users sorted by subscription months")

    def extend_subscription(self, name, surname, additional_months):
        """
        Функция для продления подписки пользователя на дополнительное количество месяцев.
        :param name: Имя пользователя
        :param surname: Фамилия пользователя
        :param additional_months: Количество месяцев для продления
        """
        for user in self.users:
            if user["name"] == name and user["surname"] == surname:
                # Рассчитываем новую дату окончания подписки
                new_end_date = user["subscription_end"] + relativedelta(months=+additional_months)
                user["subscription_end"] = new_end_date
                # Обновляем количество месяцев подписки
                user["months_subscribed"] += additional_months
                logger.debug(f"User {name} {surname} extended subscription by {additional_months} months")

    def read_from_csv(self, file_path):
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                self.add_user(row["name"], row["surname"], row["subscription_start"], row["subscription_end"],
                              int(row["months_subscribed"]))
            logger.info(f"Read {len(self.users)} users from {file_path}")

    def write_to_csv(self, file_path):
        with open(file_path, mode='w', newline='') as file:
            fieldnames = ["name", "surname", "subscription_start", "subscription_end", "months_subscribed"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for user in self.users:
                writer.writerow({
                    "name": user["name"],
                    "surname": user["surname"],
                    "subscription_start": user["subscription_start"].strftime("%d-%m-%Y"),
                    "subscription_end": user["subscription_end"].strftime("%d-%m-%Y"),
                    "months_subscribed": user["months_subscribed"]
                })
            logger.info(f"Wrote {len(self.users)} users to {file_path}")



if __name__ == "__main__":
    try:
        # Создание экземпляра класса
        music_subscriptions = MusicSubscription()

        # Добавление пользователей
        music_subscriptions.add_user("Алексей", "Петров", "01-01-2023", "01-07-2023", 6)
        music_subscriptions.add_user("Мария", "Иванова", "15-02-2023", "15-08-2023", 6)
        logger.info(f"Added two users: Алексей Петров and Мария Иванова")

        # Обновление данных пользователя
        music_subscriptions.update_user_name("Алексей", "Александр")
        music_subscriptions.update_subscription_months("Мария", "Иванова", 12)
        logger.info(f"Updated user data: Алексей changed name to Александр, Мария extended subscription to 12 months")

        # Продление подписки пользователя
        music_subscriptions.extend_subscription("Мария", "Иванова", 3)
        logger.info(f"Extended subscription of Мария Иванова by 3 months")

        # Проверка существования пользователя
        exists = music_subscriptions.check_user_exists("Александр", "Петров")
        print(f"Пользователь существует: {exists}")
        logger.debug(f"Checked if user Александр Петров exists: {exists}")

        # Сортировка пользователей
        music_subscriptions.sort_users_by_name()
        logger.debug("Sorted users by name")

        # Чтение и запись в CSV
        music_subscriptions.write_to_csv("users.csv")
        music_subscriptions.read_from_csv("users.csv")
        logger.info(f"Read and wrote users data to users.csv")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        logger.error(f"An error occurred: {e}")
