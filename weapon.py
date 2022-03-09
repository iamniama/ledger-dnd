class Weapon:
    def __init__(self, name, damage_type, damage, bonuses=0):
        self.name = name
        self.damage_type = damage_type
        self.damage = damage
        self.bonuses = bonuses

    def __str__(self):
        return (
            f'Name: {self.name}, {self.damage}{"+"+str(self.bonuses) if self.bonuses != 0 else ""} {self.damage_type}'
        )


if __name__ == "__main__":
    lsword = Weapon('longsword', 'slashing', '1d8')
    p1lsword = Weapon('longsword', 'slashing', '1d8', 1)
    print(lsword)
    print(p1lsword)