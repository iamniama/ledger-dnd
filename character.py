from dice import Dice
from weapon import Weapon


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
        self.hit_dice = int(hp.split('d')[0])
        self.advantage = False
        self.disadvantage = False
        self.inventory = []
        # self.weapons = [{'name': 'fist', 'damage': '1d4', 'type': 'bludgeoning'}]
        self.weapons = [Weapon('fist', 'bludgeoning', '1d4')]
        self.default_weapon = self.weapons[0]

    def __str__(self):
        return (f'{self.name}\n\n'
                f'Armor Class: {self.ac}\n'
                f'Hit Points: {self.hp}\n'
                f'Hit Dice: {self.hit_dice}\n'
                f'Equipped Weapon: {self.default_weapon.name}\n'
                f'Weapon Damage: {self.default_weapon.damage} +{self.str_mod}\n'
                f'Movement Speed: {self.speed}\n'
                f'Strength Bonus: {self.str_mod}\n'
                f'Intelligence Bonus: {self.int_mod}\n'
                f'Wisdom Bonus: {self.wis_mod}\n'
                f'Dexterity Bonus: {self.dex_mod}\n'
                f'Constitution Bonus: {self.con_mod}\n'
                f'Charisma Bonus: {self.cha_mod}\n'
                f'Inventory: {", ".join(self.inventory)}')

    def add_weapon(self, name, dmg_type, dmg, bonuses=0):
        self.weapons.append(Weapon(name, dmg_type, dmg, bonuses))

    def set_default_weapon(self, wpn_idx):
        self.default_weapon = self.weapons[wpn_idx]

    def add_item(self, item):
        self.inventory.append(item)

    def attack(self, other, attack_roll=Dice.text_roll('1d20')):
        if attack_roll + self.str_mod + self.default_weapon.bonuses >= other.ac:
            dmg = Dice.text_roll(self.default_weapon.damage) * 2 + self.str_mod + self.default_weapon.bonuses if attack_roll != 20 else Dice.text_roll(self.default_weapon.damage) + self.str_mod + self.default_weapon.bonuses
            other.hp -= dmg
            return f"{self.name} hits {other.name} for {dmg} {self.default_weapon.damage_type} damage"
        return f"{self.name} MISSES {other.name}"


if __name__ == "__main__":
    thing1 = Character("thing1", str_mod=2)
    thing1.add_weapon('longsword', 'slashing', '1d8', 1)
    thing1.set_default_weapon(1)
    thing2 = Character("thing2")
    thing2.add_item("300gp")
    print("++++++++++++++++++++++++++++++++++++++++++")
    print(thing1)
    print("++++++++++++++++++++++++++++++++++++++++++")
    print(thing2)
    print("++++++++++++++++++++++++++++++++++++++++++")
    print(thing1.attack(thing2))
    print("++++++++++++++++++++++++++++++++++++++++++")
    print(thing2)
