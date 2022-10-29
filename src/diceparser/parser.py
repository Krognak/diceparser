"""DiceParser implementation to parse strings into dice roll results"""

from __future__ import annotations

import re
from typing import Callable

from .dice import Dice

# matches [num(optional)]d[sides]
DICE_PATTERN = re.compile(r"(\d*)d(\d+)")
# matches [left operand][operator][right operand]
# with optional spaces around the operator
MATHS_PATTERN = re.compile(r"(?P<lhs>\w+)\s*(?P<op>[-+\/*])\s*(?P<rhs>\w+)")


class ParserError(Exception):  # pylint: disable=missing-class-docstring
    def __init__(self, string):
        self.string = string

    def __str__(self):
        return f"Unable to parse '{self.string}'"


class DiceParser:
    """Parser for standard dice notation

    Attributes:
        matches: dict with keys = Match and vals = Dice
    """

    def __init__(self):
        self.matches = None

    def _sub_dice(self, func: str, string: str) -> str:
        for k, dice in self.matches.items():
            # count = 1 so repeated dice in the same string don't roll the same value
            # e.g., 1d6 + 4 + 1d6 would roll both '1d6s' to the same value otherwise
            string = string.replace(k.group(), str(getattr(Dice, func)(dice)), 1)
        return string

    @staticmethod
    def _check_operands(string: str) -> int:
        try:
            return int(string)
        except ValueError as err:
            raise ParserError(string) from err

    def _sub_ops(self, string: str) -> str:
        m = MATHS_PATTERN.search(string)  # pylint: disable=invalid-name
        while m:
            lhs, rhs = map(self._check_operands, (m.group("lhs"), m.group("rhs")))
            opr = getop(m.group("op"))
            string = string.replace(m.group(), str(opr(lhs, rhs)))
            m = MATHS_PATTERN.search(string)  # pylint: disable=invalid-name
        return string

    def parse(self, string: str) -> None:
        """Build self.matches dict from string.

        Arguments:
            string: user-provided string contatining standard notation.

        Raises:
            ParserError: If not matches found in string.
        """
        self.matches = {d: Dice.from_match(d) for d in DICE_PATTERN.finditer(string)}
        if not self.matches:
            raise ParserError(string)

    def eval(self, func: str, string: str) -> int:
        """Evaluate maths results from string containing dice notation.

        Parses dice from string, substitutes parsed values with results from
        provided Dice method, and evaluates resultant maths expression without
        using the builtin eval function.

        Arguments:
            func: Dice method to be applied to parse dice pool.
            string: user-provided string contatining standard notation.

        Returns:
            int: Result of substituting dice notation and evaluating maths.
        """
        self.parse(string)
        string = self._sub_dice(func, string)
        string = self._sub_ops(string)
        return int(string)


def getop(opstring: str) -> Callable:
    """Maps operator string to maths function

    Division is rounded down to the nearest integer
    """
    ops = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x // y,
    }
    return ops[opstring]
