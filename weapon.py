import json

class Weapon:
    def __init__(self, name, damage_type, damage, crit_range=20, bonuses=0):
        self.name = name
        self.damage_type = damage_type
        self.damage = damage
        self.crit_range = crit_range
        self.bonuses = bonuses
        self.description = ""

    def __str__(self):
        return (
            f'Name: {self.name}, {self.damage}{"+"+str(self.bonuses) if self.bonuses != 0 else ""} {self.damage_type}'
        )

    def to_json(self):
        return json.dumps(
            {
                'NAME': self.name,
                'DAMAGE': self.damage,
                'DAMAGE_TYPE': self.damage_type,
                'BONUSES': self.bonuses,
                'DESCRIPTION': self.description
            }
        )

    def set_description(self, desc):
        self.description = desc


if __name__ == "__main__":
    lsword = Weapon('longsword', 'slashing', '1d8')
    p1lsword = Weapon('longsword', 'slashing', '1d8', 1)
    p1lsword.set_description("A finely made sword bearing faint, silvery runes of enchantment")
    print(lsword)
    print(p1lsword)
    print(p1lsword.to_json())