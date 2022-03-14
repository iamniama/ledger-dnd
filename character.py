from dice import Dice
from weapon import Weapon


class Character:
    def __init__(self, name, str_mod=0, int_mod=0, wis_mod=0, dex_mod=0, con_mod=0, cha_mod=0, ac=10, speed=30, hp="2d8"):
        """
        Initializes a Character in code.
        :param name: str, the name of the character
        :param str_mod: int, the Character's strength modifier (NOTE: these are MODIFIERS, not the stat!)
        :param int_mod: int, intelligence modifier
        :param wis_mod: int, wisdom modifier
        :param dex_mod: int, dexterity modifier
        :param con_mod: int, constitution modifier
        :param cha_mod: int, charisma modifier
        :param ac: int, the Character's armor class
        :param speed: int, distance the Character can cover in 1 round
        :param hp: str, command for Dice.text_roll
        """
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
        self.max_hp = self.hp
        self.hit_dice = int(hp.split('d')[0])
        self.hit_dice_total = self.hit_dice
        self.hit_die = int(hp.split('d')[1])
        self.advantage = False
        self.disadvantage = False
        self.inventory = []
        self.weapons = [Weapon('fist', 'bludgeoning', '1d4')]
        self.default_weapon = self.weapons[0]
        self.alive = True
        self.unconscious = False

    def __str__(self):
        """
        Outputs relevant Character data to string
        :return: str
        """
        return (f'{self.name}\n\n'
                f'Alive: {self.alive}\n'
                f'Conscious: {not self.unconscious}\n'
                f'Armor Class: {self.ac}\n'
                f'Hit Points: {self.hp}/{self.max_hp}\n'
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
        """
        Adds a new Weapon to a Character
        :param name: str, name of the weapon
        :param dmg_type: str, type of damage, slashing, piercing, bludgeoning
        :param dmg: str, Dice.text_roll command
        :param bonuses: int, positive or negative modifier
        :return: None
        """
        self.weapons.append(Weapon(name, dmg_type, dmg, bonuses))

    def set_default_weapon(self, wpn_idx):
        """
        Selects a Character's weapon to be used automatically by Character.attack
        :param wpn_idx: int, index of the weapon in self.weapons
        :return: None
        """
        self.default_weapon = self.weapons[wpn_idx]

    def add_item(self, item):
        """
        Very basic implementation of adding an item to inventory
        :param item: str, item name
        :return: None
        """
        self.inventory.append(item)

    def attack(self, other, attack_roll=Dice.text_roll('1d20')):
        """
        Executes an attack, and if successful, applies damage to the target
        :param other: Character, the target of the attack
        :param attack_roll: str, a Dice.text_roll command, defaults to 1d20 and probably won't be used in code
        :return: str, description of attack/damage outcome
        """
        if attack_roll + self.str_mod + self.default_weapon.bonuses >= other.ac:
            dmg = Dice.roll_damage(self.default_weapon.damage, attack_roll >= self.default_weapon.crit_range) \
                  + self.str_mod + self.default_weapon.bonuses
            other.take_damage(dmg)
            return (f"{self.name} {'critically ' if attack_roll >= self.default_weapon.crit_range else ''}hits!\n"
                    f"{other.name} takes {dmg} {self.default_weapon.damage_type} damage")
        return f"{self.name} MISSES {other.name}"

    def take_damage(self, dmg):
        """
        Applies damage to a Character from an attack, spell, or other source.
        Applies death or unconscious statuses as needed
        :param dmg: int, the amount of damage taken
        :return: None
        """
        self.hp -= dmg
        if -10 < self.hp < 1:
            self.unconscious = True
        elif self.hp <= -10:
            self.alive = False

    def recover_health(self, healing):
        """
        Apply healing, and update the unconscious status as needed.
        NOTE: a Character can't be healed if it is dead
        :param healing: int, amount of healing done
        :return: None
        """
        if (-10 < self.hp < 1) and (self.hp + healing >= 1):
            self.unconscious = False
        if self.alive:
            if healing + self.hp <= self.max_hp:
                self.hp += healing
            else:
                self.hp = self.max_hp

    def use_hit_dice(self, num_dice):
        """
        Recover health using Hit Dice, and update Hit Dice pool
        :param num_dice: int, the number of dice to use.  If the number is greater than the available, only the remaining
        available hit dice will be used
        :return: None
        """
        # this needs some bounds checking
        if self.alive and not self.unconscious and self.hit_dice > 0:
            if num_dice < self.hit_dice:
                self.recover_health(Dice.text_roll(f'{num_dice}d{self.hit_die}'))
            else:
                self.recover_health(Dice.text_roll(f'{self.hit_dice}d{self.hit_die}'))

    def recover_hit_dice(self, num_dice):
        """
        Regain Hit Dice, as during a Long Rest
        :param num_dice: the number of dice to recover
        :return: None
        """
        if self.hit_dice + num_dice > self.hit_dice_total:
            self.hit_dice = self.hit_dice_total
        else:
            self.hit_dice += num_dice


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
    print("++++++++++++++++++++++++++++++++++++++++++")
    thing2.recover_health(Dice.text_roll('1d8'))
    print(thing2)
    if 0 < thing2.hp < thing2.max_hp:
        print(f"{thing2.name} binds wounds...\n")
        thing2.use_hit_dice(1)
        print(thing2)
