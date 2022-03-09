from dice import Dice


class Character:
    def __init__(self, name, str_mod=0, int_mod=0, wis_mod=0, dex_mod=0, con_mod=0, cha_mod=0, ac=10, speed=30, hp="2d8"):
        self.name = name
        self.str_mod = str_mod
        self.int_mod = int_mod
        self.wis_mod = wis_mod
        self.dex_mod = dex_mod
        self.con_mod = con_mod
        self.cha_mod = cha_mod
        self.ac = ac
        self.speed = speed
        self.hp = Dice.text_roll(hp)
        self.advantage = False
        self.disadvantage = False
        self.inventory = []
        self.weapons = [{'name': 'fist', 'damage': '1d4', 'type': 'bludgeoning'}]
        self.default_weapon = self.weapons[0]

    def __str__(self):
        return (f'{self.name}\n\n'
                f'Armor Class: {self.hp}\n'
                f'Hit Points: {self.hp}\n'
                f'Equipped Weapon: {self.default_weapon["name"]}\n'
                f'Weapon Damage: {self.default_weapon["damage"]} +{self.str_mod}\n'
                f'Movement Speed: {self.speed}\n'
                f'Strength Bonus: {self.str_mod}\n'
                f'Intelligence Bonus: {self.int_mod}\n'
                f'Wisdom Bonus: {self.wis_mod}\n'
                f'Dexterity Bonus: {self.dex_mod}\n'
                f'Constitution Bonus: {self.con_mod}\n'
                f'Charisma Bonus: {self.cha_mod}\n'
                f'Inventory: {", ".join(self.inventory)}')

    def add_weapon(self, weapon):
        self.weapons.append(weapon)

    def add_item(self, item):
        self.inventory.append(item)

    def attack(self, other):
        attack_roll = Dice.roll(1,20)
        if attack_roll + self.str_mod >= other.ac:
            return f"{self.name} hits {other.name} for {Dice.roll(1,8,self.str_mod) if attack_roll != 20 else Dice.roll(2,8,self.str_mod)} damage"
        return f"{self.name} MISSES {other.name}"


if __name__ == "__main__":
    thing1 = Character("thing1", str_mod=2)
    thing2 = Character("thing2")
    thing2.add_item("300gp")
    print(thing1)
    print(thing2)
    print(thing1.attack(thing2))