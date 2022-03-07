import random
import re


class Dice:

    def __init__(self):
        pass

    @staticmethod
    def roll(dice, sides, modifier=0):
        rolls = random.choices([random.randint(1,sides) for x in range(1000)], k=dice)
        return {
            'dice': dice,
            'sides': sides,
            'rolls': rolls,
            'total_modifiers': modifier,
            'total': sum(rolls) + modifier,
        }

    @staticmethod
    def stat_roll(dice=4, highest=3):
        rolls = Dice.roll(dice, 6)['rolls']
        return {
            'rolls': list(reversed(sorted(rolls)))[:highest],
            'total': sum(list(reversed(sorted(rolls)))[:highest])
        }

    @staticmethod
    def roll_stats():
        return [Dice.stat_roll(dice=5)['total'] for x in range(6)]

    @staticmethod
    def roll_with_advantage(modifiers):
        return max([Dice.roll(1, 20, modifiers)['total'] for x in range(2)])

    @staticmethod
    def roll_with_disadvantage(modifiers):
        return min([Dice.roll(1, 20, modifiers)['total'] for x in range(2)])


if __name__ == "__main__":
    # print(Dice.roll(6,6,10))
    # print(Dice.stat_roll())
    # print(*Dice.roll_stats(), sep="\n")
    print(Dice.roll_with_advantage(-2))
