from typing import List
import csv


class Hero:
    def __init__(self) -> None:
        """
        Конструктор класса Hero.
        """
        self.heroes: List[dict] = []

    def change_class(self, new_class: str) -> None:
        """
        Изменяет класс героя.

        :param new_class: Новый класс героя.
        """
        self.hero_class: str = new_class

    def change_hp(self, new_hp: int) -> None:
        """
        Изменяет уровень здоровья героя.

        :param new_hp: Новый уровень здоровья героя.
        """
        self.hp: int = new_hp

    def change_damage(self, new_damage: int) -> None:
        """
        Изменяет урон героя.

        :param new_damage: Новый урон героя.
        """
        self.damage: int = new_damage

    def change_armor(self, new_armor: int) -> None:
        """
        Изменяет броню героя.

        :param new_armor: Новый уровень брони героя.
        """
        self.armor: int = new_armor

    def change_lvl(self, new_lvl: int) -> None:
        """
        Изменяет уровень героя.

        :param new_lvl: Новый уровень героя.
        """
        self.lvl: int = new_lvl

    def hero_exists(self, id: int) -> bool:
        """
        Проверяет существование героя с указанным ID.

        :param id: Уникальный идентификатор героя.

        :return: True, если герой с указанным ID существует, иначе False.

        :raises ValueError: В случае отсутствия героя с указанным ID.
        """
        for hero in self.heroes:
            if hero['id'] == id:
                return True
        raise ValueError("Герой с указанным ID не найден")

    def can_survive(self, id: int) -> bool:
        """
        Проверяет способность героя выжить в бою в соответствии с заданными условиями.

        :param id: Уникальный идентификатор героя.

        :return: True, если герой может выжить в бою, иначе False.

        :raises ValueError: В случае отсутствия героя с указанным ID.
        """
        for hero in self.heroes:
            if hero['id'] == id:
                if hero['lvl'] >= 5 and hero['hp'] > 80 and hero['damage'] > 25:
                    return True
                else:
                    return False
        raise ValueError("Герой с указанным ID не найден")

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
        Добавляет нового героя в список героев.

        :param id: Уникальный идентификатор героя.
        :param hero_class: Класс героя.
        :param hp: Здоровье героя.
        :param damage: Урон героя.
        :param armor: Броня героя.
        :param lvl: Уровень героя.
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

    def remove_hero(self, id: int) -> None:
        """
        Удаляет героя из списка по указанному ID.

        :param id: Уникальный идентификатор героя.
        """
        for hero in self.heroes:
            if hero['id'] == id:
                self.heroes.remove(hero)
                break

    def sort_by_hp(self) -> None:
        """Сортирует список героев по уровню здоровья, в порядке убывания."""
        self.heroes.sort(key=lambda x: x['hp'], reverse=True)

    def sort_by_lvl(self) -> None:
        """Сортирует список героев по уровню, в порядке убывания."""
        self.heroes.sort(key=lambda x: x['lvl'], reverse=True)

    def read_from_csv(self, file_name: str) -> None:
        """
        Загружает данные о героях из CSV-файла и добавляет их в список героев.

        :param file_name: Имя CSV-файла.
        """
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                id, hero_class, hp, damage, armor, lvl = row
                self.add_hero(int(id), hero_class, int(
                    hp), int(damage), int(armor), int(lvl))

    def write_to_csv(self, file_name: str) -> None:
        """
        Записывает данные о героях в CSV-файл.

        :param file_name: Имя CSV-файла.
        """
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            for hero in self.heroes:
                writer.writerow([hero['id'], hero['hero_class'], hero['hp'],
                                hero['damage'], hero['armor'], hero['lvl']])


if __name__ == "__main__":
    try:
        Heroes = Hero()

        Heroes.add_hero(6, 'Mage', 80, 30, 5, 7)
        Heroes.add_hero(7, 'Rogue', 90, 25, 8, 6)
        Heroes.add_hero(8, 'Paladin', 120, 20, 15, 8)
        Heroes.add_hero(9, 'Druid', 110, 25, 10, 9)
        Heroes.add_hero(10, 'Hunter', 100, 35, 5, 7)
        Heroes.add_hero(11, 'Shaman', 95, 30, 7, 3)
        Heroes.add_hero(12, 'Warlock', 85, 40, 3, 9)

        print(Heroes.can_survive(12))
        print(Heroes.can_survive(11))
        print(Heroes.can_survive(7))

        Heroes.sort_by_hp()
        Heroes.sort_by_lvl()

        Heroes.write_to_csv('sorted_heroes.csv')
    except Exception as e:
        print(f"An error occurred: {e}")
