import random
import re


class Dice:
    """
    A set of static methods to accomplish various dice rolls using the builtin random library.
    Rather than futz with other random libraries, I decided that the base method (roll) should
    generate a significant number of rolls (1000) and select random values from among them based
    on the number of dice
    """
    dice_pool = 1000

    def __init__(self):
        pass

    @staticmethod
    def roll(dice, sides, modifiers=0):
        """
        The core of the Dice library, roll generates 1000 random numbers in the given range (sides) and selects
        a given number (dice) of values to return.
        :param dice: how many random nums to keep
        :param sides: upper limit of individual randoms
        :param modifiers: a positive or negative in that affects the value of the roll, defaults to 0
        :return: dict with the number of dice, number of sides, values of each individual die, the value of
        modifier, and an aggregated total of the roll
        """
        rolls = random.choices([random.randint(1,sides) for x in range(Dice.dice_pool)], k=dice)
        return {
            'dice': dice,
            'sides': sides,
            'rolls': rolls,
            'total_modifiers': modifiers,
            'total': sum(rolls) + modifiers,
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
    def roll_with_advantage(modifiers=0):
        """
        Performs an attack or skill check with advantage, wherein two 20 sided dice are rolled, and the higher value
        is kept
        :param modifiers: total value of hit or check modifiers, defaults to 0
        :return: integer, highest of two rolls plus the value of modifiers
        """
        return max([Dice.roll(1, 20, modifiers)['total'] for x in range(2)])

    @staticmethod
    def roll_with_disadvantage(modifiers=0):
        """
        Performs an attack or skill check with disadvantage, wherein two 20 sided dice are rolled, and the lower value
        is kept
        :param modifiers: total value of hit or check modifiers, defaults to 0
        :return: integer, lowest of two rolls plus the value of modifiers
        """
        return min([Dice.roll(1, 20, modifiers)['total'] for x in range(2)])

    @staticmethod
    def multi_roll(lst_dice, modifiers=0):
        """
        Shorthand method for rolls that involve multiple dice, such as a flametongue sword,
        which does 1d8 for the sword and 2d6 for the fire damage while activated
        :param lst_dice: an array of strings in the format XdY (1d6, 2d8, etc) to denote part of the total roll
        :param modifiers: int, added to the total. defaults to 0
        :return: int, sum of dice rolls and modifiers
        """
        total = 0
        for x in lst_dice:
            dice, sides = [int(y) for y in x.split('d')]
            total += Dice.roll(dice, sides)['total']
        return total + modifiers


if __name__ == "__main__":
    print("\n****************Base Roll***************************")
    print(Dice.roll(6,6,10))
    print("\n****************Stat Roll***************************")
    print(Dice.stat_roll())
    print("\n****************Roll Stats***************************")
    print(*Dice.roll_stats(), sep="\n")
    print("\n****************Advantage Roll***************************")
    print(Dice.roll_with_advantage(-2))
    print("\n****************Multi Roll***************************")
    print(Dice.multi_roll(['1d8', '2d6'], 5))
