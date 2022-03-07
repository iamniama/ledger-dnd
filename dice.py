import random
import re


class Dice:

    def __init__(self):
        pass

    @staticmethod
    def roll(dice, sides, modifier=0):
        """
        The core of the Dice library, roll generates 1000 random numbers in the given range (sides) and selects
        a given number (dice) of values to return.
        :param dice: how many random nums to keep
        :param sides: upper limit of individual randoms
        :param modifier: a positive or negative in that affects the value of the roll
        :return: dict with the number of dice, number of sides, values of each individual die, the value of
        modifier, and an aggregated total of the roll
        """
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
        """
        Rolls a given number of six sided dice, and keeps the highest (default 3) values
        :param dice: how many total d6 to roll, defaults to 4 per 5E rules
        :param highest: how many dice to keep, defaults to 3 per 5E rules
        :return: dict with list of individual kept dice values and the total of the kept dice
        """
        rolls = Dice.roll(dice, 6)['rolls']
        return {
            'rolls': list(reversed(sorted(rolls)))[:highest],
            'total': sum(list(reversed(sorted(rolls)))[:highest])
        }

    @staticmethod
    def roll_stats():
        """
        Generates a full set of stat rolls for a new character.  In the initial version, this uses one of my
        old house rules that uses 5 dice instead of the stated 4 from the 5E rules.
        :return: list of six outputs from stat_roll
        """
        return [Dice.stat_roll(dice=5)['total'] for x in range(6)]

    @staticmethod
    def roll_with_advantage(modifiers):
        """
        Performs an attack or skill check with advantage, wherein two 20 sided dice are rolled, and the higher value
        is kept
        :param modifiers: total value of hit or check modifiers
        :return: integer, highest of two rolls plus the value of modifiers
        """
        return max([Dice.roll(1, 20, modifiers)['total'] for x in range(2)])

    @staticmethod
    def roll_with_disadvantage(modifiers):
        """
        Performs an attack or skill check with disadvantage, wherein two 20 sided dice are rolled, and the lower value
        is kept
        :param modifiers: total value of hit or check modifiers
        :return: integer, lowest of two rolls plus the value of modifiers
        """
        return min([Dice.roll(1, 20, modifiers)['total'] for x in range(2)])


if __name__ == "__main__":
    # print(Dice.roll(6,6,10))
    # print(Dice.stat_roll())
    # print(*Dice.roll_stats(), sep="\n")
    print(Dice.roll_with_advantage(-2))
