"""Yet another dice-parsing module!

Parsing and common functions for standard dice notation of the form [num]d[sides].

Usage:
>>> import diceparser
>>> parser = diceparser.DiceParser()
>>> parser.eval("roll", "3d6+1")
9
"""

from .parser import DiceParser
from .dice import Dice
