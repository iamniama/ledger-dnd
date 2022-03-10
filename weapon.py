import json


class Weapon:
    def __init__(self, name, damage_type, damage, crit_range=20, bonuses=0):
        """
        Initializes a Weapon based on inputs
        :param name: str, right now I'm using this for weapon type, need to flesh this out more
        :param damage_type: str, type of damage (slashing, bludgeoning, etc)
        :param damage: str, Dice.text_roll command
        :param crit_range: int, Attack rolls equaling or exceeding this value are deemed critical attacks
        :param bonuses: int,magical or other modifiers, usually positive
        """
        self.name = name
        self.damage_type = damage_type
        self.damage = damage
        self.crit_range = crit_range
        self.bonuses = bonuses
        self.description = ""

    @staticmethod
    def from_json(filename):
        """
        Creates a new Weapon from a JSON file
        :param filename: str, the name of the JSON file
        :return: Weapon object with properties from the JSON
        """
        with open(filename, 'r') as infile:
            wpn_data = json.load(infile)
            wpn = Weapon(wpn_data['name'], wpn_data['damage_type'], wpn_data['damage'], wpn_data['crit_range'], wpn_data['bonuses'])
            wpn.set_description(wpn_data['description'])
            return wpn

    def __str__(self):
        """
        String output of Weapon
        :return: str, properties condensed into a strin
        """
        return (
            f'Name: {self.name}, {self.damage}{"+"+str(self.bonuses) if self.bonuses != 0 else ""} {self.damage_type}\n'
            f'{self.description}\n'
        )

    def to_json(self):
        """
        Dumps Weapon to JSON
        :return: JSON of Weapon
        """
        return json.dumps(
            {
                'name': self.name,
                'damage': self.damage,
                'crit_range': self.crit_range,
                'damage_type': self.damage_type,
                'bonuses': self.bonuses,
                'description': self.description
            }
        )

    def write_to_file(self, filename):
        """
        Outputs JSON to a file
        :param filename: str, filename to use
        :return: None
        """
        with open(filename, 'w') as outfile:
            outfile.write(self.to_json())

    def set_description(self, desc):
        """
        Set description of a weapon
        :param desc:
        :return:
        """
        self.description = desc


if __name__ == "__main__":
    lsword = Weapon('longsword', 'slashing', '1d8')
    p1lsword = Weapon('longsword', 'slashing', '1d8', bonuses=1)
    p1lsword.set_description("A finely made sword bearing faint, silvery runes of enchantment")
    print(lsword)
    print(p1lsword)
    print(p1lsword.to_json())
    p1lsword.write_to_file('plus1sword.json')
    sword2 = Weapon.from_json('plus1sword.json')
    print(sword2)
