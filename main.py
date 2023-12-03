import csv
import logging
from typing import List


class Product:
    def __init__(
        self, name: str, price: float, quantity: int, expiration_date: str
    ) -> None:
        """
        Initialize a Product object with name, price, quantity, and expiration date.
        """
        self.name = name
        self.price = price
        self.quantity = quantity
        self.expiration_date = expiration_date
        self.logger = self.set_logger()

    def set_logger(self):
        """
        Installation function logger
        """
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            file_handler = logging.FileHandler("product_log.log")
            file_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        return logger

    def change_name(self, new_name: str) -> None:
        """
        Change the name of the product.
        """
        self.name = new_name
        self.logger.info(f"The product name has been changed: {new_name}")

    def change_price(self, new_price: float) -> None:
        """
        Change the price of the product.
        """
        self.price = new_price
        self.logger.info(f"The price of the product has been changed: {new_price}")

    def change_quantity(self, new_quantity: int) -> None:
        """
        Change the quantity of the product.
        """
        self.quantity = new_quantity
        self.logger.info(
            f"The quantity of the product has been changed: {new_quantity}"
        )

    def change_expiration_date(self, new_date: str) -> None:
        """
        Change the expiration date of the product.
        """
        self.expiration_date = new_date
        self.logger.info(
            f"The expiration date of the product has been changed: {new_date}"
        )


class ProductStore:
    def __init__(self) -> None:
        """
        Initialize a ProductStore object with an empty list of products.
        """
        self.products: List[Product] = []
        self.logger = self.set_logger()

    def set_logger(self):
        """
        Installation function logger
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler("product_log.log")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def product_exists(self, product_name: str) -> bool:
        """
        Check if a product with the given name already exists in the inventory.
        Returns True if the product exists, False otherwise.
        """
        for product in self.products:
            if product.name == product_name:
                self.logger.info(f"The product {product_name} exists")
                return True
        self.logger.info(f"The product {product_name} does not exist")
        return False

    def add_product(self, product: Product) -> bool:
        """
        Add a new product to the inventory if it doesn't already exist.
        Returns True if the product was added, False otherwise.
        """
        if not self.product_exists(product.name):
            self.products.append(product)
            self.logger.info(f"The product {product.name} has been added")
            return True
        self.logger.info(
            f"The product {product.name} has not been added because it is already there"
        )
        return False

    def sort_by_price(self) -> None:
        """
        Sort the products in the inventory by price in ascending order.
        """
        self.products.sort(key=lambda x: x.price, reverse=False)
        self.logger.info(f"Products sorted by price in ascending order")

    def sort_by_revers_price(self) -> None:
        """
        Sort the products in the inventory by price in descending order.
        """
        self.products.sort(key=lambda x: x.price, reverse=True)
        self.logger.info(f"Products sorted by price in descending order")

    def sort_by_quantity(self) -> None:
        """
        Sort the products in the inventory by quantity in ascending order.
        """
        self.products.sort(key=lambda x: x.quantity, reverse=False)
        self.logger.info(f"Products sorted by quantity in ascending order")

    def sort_by_revers_quantity(self) -> None:
        """
        Sort the products in the inventory by quantity in descending order.
        """
        self.products.sort(key=lambda x: x.quantity, reverse=True)
        self.logger.info(f"Products sorted by quantity in descending order")

    def read_from_csv(self, file_name: str) -> None:
        """
        Read product data from a CSV file and add it to the inventory.
        """
        try:
            with open(file_name, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    name, price, quantity, expiration_date = row
                    product = Product(
                        name, float(price), int(quantity), expiration_date
                    )
                    self.products.append(product)
            self.logger.info(f"Products read from CSV file {file_name}")
        except FileNotFoundError:
            self.logger.warning(f"File {file_name} not found")

    def write_to_csv(self, file_name: str) -> None:
        """
        Write the product data from the inventory to a CSV file.
        """
        try:
            with open(file_name, "w", newline="") as file:
                writer = csv.writer(file)
                for product in self.products:
                    writer.writerow(
                        [
                            product.name,
                            product.price,
                            product.quantity,
                            product.expiration_date,
                        ]
                    )
            self.logger.info(f"Products are written to a CSV file {file_name}")
        except FileNotFoundError:
            self.logger.warning(f"File {file_name} not found")

    def print_products(self) -> None:
        """
        Print information about all the products in the inventory.
        """
        self.logger.info("Printing products")
        for product in self.products:
            self.logger.debug(
                f"Product: {product.name}, Price: {product.price}, Quantity: {product.quantity}, Expiration Date: {product.expiration_date}"
            )
        self.logger.info("Printed all products")

    def clear_products(self):
        self.products = []
        self.logger.info("Cleared all products")


if __name__ == "__main__":
    try:
        store = ProductStore()

        store.read_from_csv("products.csv")
        store.add_product(Product("Milk", 2.5, 10, "2023-01-01"))
        store.add_product(Product("Apple", 1, 5, "2023-01-01"))
        store.add_product(Product("Shit", 0.11, 10, "2023-01-01"))
        store.add_product(Product("Water", 0.1, 30, "2023-01-01"))
        store.add_product(Product("Watermelon", 3, 7, "2023-01-01"))
        store.add_product(Product("Melon", 8, 9, "2023-01-01"))
        store.add_product(Product("Milk", 2.5, 10, "2023-01-01"))
        store.add_product(Product("nuts", 2.5, 10, "2023-01-01"))

        pr1 = Product("Milk", 2.5, 10, "2023-01-01")
        pr1.change_price(30)

        store.print_products()
        store.sort_by_price()
        store.sort_by_revers_price()
        store.sort_by_quantity()
        store.sort_by_revers_quantity()

        store.write_to_csv("updated_products.csv")
        store.clear_products()
    except Exception as error:
        logging.exception("Произошла ошибка", exc_info=True)
