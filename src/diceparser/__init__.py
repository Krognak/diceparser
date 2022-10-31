"""Yet another dice-parsing module!

Parsing and common functions for standard dice notation of the form [num]d[sides].

Usage:
>>> import diceparser
>>> parser = diceparser.DiceParser()
>>> parser.eval("roll", "3d6+1")
9
"""

from .dice import Dice
from .parser import DiceParser

__version__ = "0.2.0"
