import random
import re


class Dice:
    """
    A set of static methods to accomplish various dice rolls using the builtin random library.
    Rather than futz with other random libraries, I initially decided that the base method (roll) should
    generate a significant number of rolls (1000) and select random values from among them based
    on the number of dice, but decided to scale the pool to dice_pool (defaults to 50) * number of dice.
    """
    dice_pool = 50
    dice_rex = re.compile(r'''
                (?P<base_roll>(?P<num_dice>[0-9]*)d(?P<sides>[0-9]{,3}))  # get the base roll, dice, and sides
            ''', re.X)
    mod_rex = re.compile(r'[+-][0-9]+\b')

    @staticmethod
    def roll(dice, sides, modifiers=0):
        """
        The core of the Dice library, roll generates random numbers (scaled based on the number of dice) in the given
        range (sides) and selects a given number (dice) of values to return.
        :param dice: how many random nums to keep
        :param sides: upper limit of individual randoms
        :param modifiers: a positive or negative int that affects the value of the roll, defaults to 0
        :return: int, sum of dice rolls and modifiers
        """
        return sum(random.choices([random.randint(1,sides) for x in range(Dice.dice_pool * dice)], k=dice)) + modifiers

    @staticmethod
    def text_roll(cmd_str):
        """
        text_roll interprets a natural language dice syntax, such as "4d4 +4" or "1d8
        :param cmd_str: text input in the format of a D&D dice roll, ie "3d6 + 3" or "1d8 +2d6 +3 +1 -1
        :return: output of multi_roll with parameters extracted from cmd_str
        """
        d_info = Dice.dice_rex.findall(cmd_str)
        modifiers = [int(x) for x in list(Dice.mod_rex.findall(cmd_str))]
        return Dice.multi_roll([a[0] for a in d_info], sum(modifiers))

    @staticmethod
    def stat_roll(dice=4, highest=3):
        """
        Rolls a given number of six sided dice, and keeps the highest (default 3) values
        :param dice: how many total d6 to roll, defaults to 4 per 5E rules
        :param highest: how many dice to keep, defaults to 3 per 5E rules
        :return: int, sum of kept dice
        """
        rolls = [Dice.roll(1, 6) for x in range(dice)]
        return sum(list(reversed(sorted(rolls)))[:highest])

    @staticmethod
    def roll_stats():
        """
        Generates a full set of stat rolls for a new character.  In the initial version, this uses one of my
        old house rules that used 5 dice instead of the stated 4 from the 5E rules.
        :return: list of six outputs from stat_roll
        """
        return [Dice.stat_roll(dice=5) for x in range(6)]

    @staticmethod
    def roll_with_advantage(modifiers=0, disadvantage=False):
        """
        Performs an attack or skill check with advantage, wherein two 20 sided dice are rolled and the higher value
        is kept, or disadvantage, which uses the lower of the two values
        :param modifiers: total value of hit or check modifiers, defaults to 0
        :param disadvantage: toggles the method to return a roll with disadvantage instead of advantage
        :return: integer, highest or lowest of two rolls plus the value of modifiers
        """
        if disadvantage:
            return min([Dice.roll(1, 20, modifiers) for x in range(2)])
        return max([Dice.roll(1, 20, modifiers) for x in range(2)])

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
            dice_and_sides = x.split('d')
            if dice_and_sides[0].isdigit():
                dice, sides = [int(y) for y in dice_and_sides]
            else:
                dice = 1
                sides = int(dice_and_sides[1])
            total += Dice.roll(dice, sides)
        return total + modifiers


if __name__ == "__main__":
    # print("\n****************Base Roll (6d6 + 10)***************************")
    # print(Dice.roll(6,6,10))
    # print("\n****************Stat Roll***************************")
    # print(Dice.stat_roll())
    # print("\n****************Roll Stats***************************")
    # print(*Dice.roll_stats(), sep="\n")
    # print("\n****************Advantage Roll***************************")
    # print(Dice.roll_with_advantage(-2))
    # print("\n****************Multi Roll d8 and 2d6***************************")
    # print(Dice.multi_roll(['1d8', '2d6'], 5))
    # print("\n****************Natural Language Roll***************************")
    # print("Command: 'd8 +2 +1 +2d6 -1'")
    # print(Dice.text_roll("d8 +2 +1 +2d6 -1"))
    # print("***********************************************")
    # print("\t\t\t\tStat Rolls")
    # for _ in range(4):
    #     print("***********************************************")
    #     print(*Dice.roll_stats(), sep="\n")
    # print("***********************************************")
    print(*Dice.roll_stats(), sep="\n")
