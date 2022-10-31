"""Dice object implementation with standard functions"""

from __future__ import annotations

from dataclasses import dataclass
from random import randint
from typing import Match, Optional


@dataclass()
class Dice:
    """A pool of dice, each with the same number of sides

    Attributes:
        num: Number of dice in pool.
        sides: Number of sides on each die.
    """

    num: int
    sides: int

    @classmethod
    def from_match(cls, match: Match) -> Dice:
        """Used by DiceParser to instantiate Dice objects from matches.

        Returns:
            Dice object with counted attrs from match.
        """
        return cls(*map(count_dice_attr, match.groups()))

    def roll(self) -> int:
        """Randomly determines a result between 1 and self.sides for each die in the
        pool.

        Returns:
            int: sum of random values
        """
        return sum((randint(1, self.sides) for _ in range(self.num)))

    def average(self) -> int:
        """Averages using the standard result av(n) = n(n+1)/2.

        The returned value is rounded down to the nearest integer value.

        Returns:
            int: The average result of rolling the dice pool."""
        return self.num * (self.sides + 1) // 2

    def min(self) -> int:
        return sum((1 for _ in range(self.num)))

    def max(self) -> int:
        return sum((self.sides for _ in range(self.num)))

# Allows for the 'lazy' notation d[sides]
def count_dice_attr(attr: Optional[str] = None) -> int:
    """CEquivalent to int(attr) if attr can be counted.

    Arguments:
        attr Optional[str]: string to be counted.

    Returns:
        int: integer with minimum of 1.
    """
    if attr:
        return int(attr)
    return 1
