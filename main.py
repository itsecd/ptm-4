import csv


class Hero:
    def __init__(self):
        self.heroes = []

    def change_class(self, new_class):
        self.hero_class = new_class

    def change_hp(self, new_hp):
        self.hp = new_hp

    def change_damage(self, new_damage):
        self.damage = new_damage

    def change_armor(self, new_armor):
        self.armor = new_armor

    def change_lvl(self, new_lvl):
        self.lvl = new_lvl

    def hero_exists(self, id):
        for hero in self.heroes:
            if hero['id'] == id:
                return True
        raise ValueError("Герой с указанным ID не найден")

    def can_survive(self, id):
        for hero in self.heroes:
            if hero['id'] == id:
                if hero['lvl'] >= 5 and hero['hp'] > 80 and hero['damage'] > 25:
                    return True
                else:
                    return False
        raise ValueError("Герой с указанным ID не найден")

    def add_hero(
        self,
        id,
        hero_class,
        hp,
        damage,
        armor,
        lvl,
    ) -> None:
        new_student = {
            "id": id,
            "hero_class": hero_class,
            "hp": hp,
            "damage": damage,
            "armor": armor,
            "lvl": lvl,
        }
        self.heroes.append(new_student)

    def remove_hero(self, id):
        for hero in self.heroes:
            if hero.id == id:
                self.heroes.remove(hero)
                return

    def sort_by_hp(self):
        self.heroes.sort(key=lambda x: x['hp'], reverse=True)

    def sort_by_lvl(self):
        self.heroes.sort(key=lambda x: x['lvl'], reverse=True)

    def read_from_csv(self, file_name):
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                id, hero_class, hp, damage, armor, lvl = row
                hero = Hero(int(id), hero_class, int(hp),
                            int(damage), int(armor), int(lvl))
                self.add_hero(hero)

    def write_to_csv(self, file_name):
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            for hero in self.heroes:
                writer.writerow([hero['id'], hero['hero_class'],
                                hero['hp'], hero['damage'], hero['armor'], hero['lvl']])


if __name__ == "__main__":
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
