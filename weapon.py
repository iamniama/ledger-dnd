import json


class Weapon:
    def __init__(self, name, damage_type, damage, crit_range=20, bonuses=0):
        self.name = name
        self.damage_type = damage_type
        self.damage = damage
        self.crit_range = crit_range
        self.bonuses = bonuses
        self.description = ""

    @staticmethod
    def from_json(filename):
        with open(filename, 'r') as infile:
            wpn_data = json.load(infile)
            return Weapon(wpn_data['name'], wpn_data['damage_type'], wpn_data['damage'], wpn_data['crit_range'], wpn_data['bonuses'])

    def __str__(self):
        return (
            f'Name: {self.name}, {self.damage}{"+"+str(self.bonuses) if self.bonuses != 0 else ""} {self.damage_type}\n'
            'A finely made sword bearing faint, silvery runes of enchantment'
        )

    def to_json(self):
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
        with open(filename, 'w') as outfile:
            outfile.write(self.to_json())

    def set_description(self, desc):
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