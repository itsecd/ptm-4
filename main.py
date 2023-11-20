import logging
import csv


class ShopInventory:
    def __init__(self) -> None:
        self.inventory = []
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler('inventory_log.log')
        file_handler.setLevel(logging.DEBUG)

        return logger

    def add_item(self, item: str) -> None:
        self.inventory.append(item)

    def remove_item(self, item: str) -> None:
        if item in self.inventory:
            self.inventory.remove(item)
            print(f"Товар удален: {item}")
        else:
            print("error!")

    def display_inventory(self) -> None:
        for item in self.inventory:
            print(item)

    def count_items(self) -> int:
        count = len(self.inventory)
        self.logger.info(f"Общее количество товаров: {count}")
        return count

    def check_item_exists(self, item: str) -> bool:
        exists = item in self.inventory
        if exists:
            print(f"Товар '{item}' присутствует в инвентаре.")
        else:
            print(f"Товар '{item}' отсутствует в инвентаре.")
        return exists

    def save_to_csv(self, filename: str = 'inventory.csv') -> None:
        try:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Товары'])
                for item in self.inventory:
                    writer.writerow([item])
        except FileNotFoundError:
            print(f"Файл {filename} не найден!")

    def load_from_csv(self, filename='inventory.csv') -> None:
        try:
            with open(filename, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Пропускаем заголовок
                self.inventory = [row[0] for row in reader]
        except FileNotFoundError:
            print(f"Файл {filename} не найден!")

    def bubble_sort_inventory(self):
        n = len(self.inventory)
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if self.inventory[j] > self.inventory[j + 1]:
                    self.inventory[j], self.inventory[j + 1] = self.inventory[j + 1], self.inventory[j]
        print("Инвентарь отсортирован методом сортировки пузырьком.")

    def search_item_by_name(self, partial_name: str) -> list[str]:
        matching_items = [item for item in self.inventory if partial_name.lower() in item.lower()]
        if matching_items:
            print(f"Найдены товары с частью названия '{partial_name}': {matching_items}")
        else:
            print(f"Товары с частью названия '{partial_name}' не найдены.")
        return matching_items

    def clear_inventory(self):
        self.inventory = []
        self.logger.info("Инвентарь очищен.")

if __name__ == "__main__":
    try:
        shop = ShopInventory()
        shop.add_item("Книга")
        shop.add_item("Фрукты")
        shop.add_item("Электроника")
        shop.add_item("Компьютер")
        shop.add_item("Фотоаппарат")
        shop.add_item("Обувь")
        shop.add_item("Вода")
        shop.add_item("Лопата)")

        shop.display_inventory()
        shop.count_items()

        shop.search_item_by_name("Обувь")
        shop.search_item_by_name("ноутбук")
        shop.search_item_by_name("Яблоко")
        shop.search_item_by_name("Книга")
        shop.clear_inventory()
        shop.display_inventory()
        shop.count_items()

    except Exception as e:
        logging.exception("Произошла ошибка", exc_info=True)
