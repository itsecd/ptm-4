from typing import List
import csv
import logging


class Heroes:
    def __init__(self) -> None:
        """
        Constructor of the Hero class.
        """
        self.heroes: List[dict] = []
        self.logger = self.set_logger()
        self.logger.info("Heroes instance created")

    def set_logger(self):
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            file_handler = logging.FileHandler("Heroes_log.log")
            file_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        return logger

    def change_class(self, new_class: str) -> None:
        """
        Changes the class of the hero.

        :param new_class: New hero class.
        """
        self.hero_class: str = new_class
        self.logger.info(f"Changed the hero class to {new_class}")

    def change_hp(self, new_hp: int) -> None:
        """
        Changes the hero's health level.

        :param new_hp: A new level of hero's health.
        """
        self.hp: int = new_hp
        self.logger.info(f"Changed the hero's health level to {new_hp}")

    def change_damage(self, new_damage: int) -> None:
        """
        Modifies the hero's damage.

        :param new_damage: New hero damage.
        """
        self.damage: int = new_damage
        self.logger.info(f"Hero damage changed to {new_damage}")

    def change_armor(self, new_armor: int) -> None:
        """
        Changes the hero's armor.

        :param new_armor: A new level of hero armor.
        """
        self.armor: int = new_armor
        self.logger.info(f"Changed the hero's armor level to {new_armor}")

    def change_lvl(self, new_lvl: int) -> None:
        """
        Changes the hero's level.

        :param new_lvl: New hero level.
        """
        self.lvl: int = new_lvl
        self.logger.info(f"Hero level changed to {new_lvl}")

    def hero_exists(self, id: int) -> bool:
        """
        Checks the existence of a hero with the specified ID.

        :param id: The unique identifier of the hero.

        :return: True if the hero with the specified ID exists, otherwise False.

        :raises ValueError: If there is no hero with the specified ID.
        """
        for hero in self.heroes:
            if hero['id'] == id:
                self.logger.info(f"Hero with ID: {id} successfully found")
                return True
            self.logger.error("Hero with specified ID not found")
            raise ValueError("Hero with specified ID not found")

    def can_survive(self, id: int) -> bool:
        """
        Checks the hero's ability to survive in battle in accordance with the specified conditions.

        :param id: The unique identifier of the hero.

        :return: True if the hero can survive the battle, otherwise False.

        :raises ValueError: If there is no hero with the specified ID.
        """
        for hero in self.heroes:
            if hero['id'] == id:
                if hero['lvl'] >= 5 and hero['hp'] > 80 and hero['damage'] > 25:
                    self.logger.info(f"Hero with ID: {id} won")
                    return True
                else:
                    self.logger.info(f"Hero with ID: {id} die")
                    return False
        self.logger.error("The hero with the specified ID was not found")
        raise ValueError("The hero with the specified ID was not found")

    def add_hero(
        self,
        id: int,
        hero_class: str,
        hp: int,
        damage: int,
        armor: int,
        lvl: int
    ) -> None:
        """
        Adds a new hero to the list of heroes.

        :param id: The unique identifier of the hero.
        :param hero_class: Hero class.
        :param hp: Hero's health.
        :param damage: Hero damage.
        :param armor: Hero's armor.
        :param lvl: Hero level.
        """
        new_hero = {
            "id": id,
            "hero_class": hero_class,
            "hp": hp,
            "damage": damage,
            "armor": armor,
            "lvl": lvl
        }
        self.heroes.append(new_hero)
        self.logger.info(f"Added a new hero with ID {id}")

    def remove_hero(self, id: int) -> None:
        """
        Removes the hero from the list by the specified ID.

        :param id: The unique identifier of the hero.
        """
        for hero in self.heroes:
            if hero['id'] == id:
                self.heroes.remove(hero)
                self.logger.info(f"Deleted hero with ID {id}")
                break

    def sort_by_hp(self) -> None:
        """ Sorts the list of heroes by health level, in descending order."""
        self.heroes.sort(key=lambda x: x['hp'], reverse=True)
        self.logger.info("The list of heroes is sorted by health level")

    def sort_by_lvl(self) -> None:
        """ Sorts the list of heroes by level, in descending order."""
        self.heroes.sort(key=lambda x: x['lvl'], reverse=True)
        self.logger.info("The list of heroes is sorted by level")

    def read_from_csv(self, file_name: str) -> None:
        """
        Loads data about heroes from a CSV file and adds them to the list of heroes.

        :param file_name: The name of the CSV file.
        """
        try:
            with open(file_name, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.heros.append(row)
            self.logger.info(f"Hero data uploaded from CSV file {file_name}")
        except Exception as e:
            self.logger.warning(f"Error reading CSV file: {file_name} - {e}")

    def write_to_csv(self, file_name: str) -> None:
        """
        Writes data about the heroes to a CSV file.

        :param file_name: The name of the CSV file.
        """
        try:
            with open(file_name, 'w', newline='') as file:
                fieldnames = [
                    "id",
                    "hero_class",
                    "hp",
                    "damage",
                    "armor",
                    "lvl"
                ]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for hero in self.heroes:
                    writer.writerow(hero)
            self.logger.info(f"Clients written to CSV file: {file_name}")
        except Exception as e:
            self.logger.warning(
                f"Error writing to CSV file: {file_name} - {e}")


if __name__ == "__main__":
    try:
        heroes = Heroes()

        heroes.add_hero(6, 'Mage', 80, 30, 5, 7)
        heroes.add_hero(7, 'Rogue', 90, 25, 8, 6)
        heroes.add_hero(8, 'Paladin', 120, 20, 15, 8)
        heroes.add_hero(9, 'Druid', 110, 25, 10, 9)
        heroes.add_hero(10, 'Hunter', 100, 35, 5, 7)
        heroes.add_hero(11, 'Shaman', 95, 30, 7, 3)
        heroes.add_hero(12, 'Warlock', 85, 40, 3, 9)

        logging.info(heroes.can_survive(12))
        logging.info(heroes.can_survive(11))
        logging.info(heroes.can_survive(7))

        heroes.sort_by_hp()
        heroes.sort_by_lvl()

        heroes.write_to_csv('sorted_heroes.csv')
    except Exception as e:
        logging.error(f"An error occurred: {e}")
