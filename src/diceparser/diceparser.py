from __future__ import annotations

import re
from dataclasses import dataclass
from random import randint
from typing import Callable, Match, Optional

DICE_PATTERN = re.compile(r"(\d*)d(\d+)")
MATHS_PATTERN = re.compile(r"(?P<lhs>\w+)\s*(?P<op>[-+\/*])\s*(?P<rhs>\w+)")


class ParserError(Exception):
    def __init__(self, string):
        self.string = string

    def __str__(self):
        return f"Unable to parse '{self.string}'"


@dataclass()
class Dice:
    num: int
    sides: int

    @classmethod
    def from_match(cls, match: Match) -> Dice:
        return cls(*map(count_dice_attr, match.groups()))

    def roll(self) -> int:
        return sum((randint(1, self.sides) for _ in range(self.num)))

    def average(self) -> int:
        return self.num * (self.sides + 1) // 2


class DiceParser:
    def __init__(self):
        self.matches = None

    def _sub_dice(self, func, string) -> str:
        for k, dice in self.matches.items():
            # count = 1 so repeated dice in the same string don't roll the same value
            # e.g., 1d6 + 4 + 1d6 would evaluate both '1d6s' to the same value
            # if count = -1
            string = string.replace(k.group(), str(getattr(Dice, func)(dice)), 1)
        return string

    @staticmethod
    def _check_operands(string) -> int:
        try:
            return int(string)
        except ValueError as err:
            raise ParserError(string) from err

    def _sub_ops(self, string) -> str:
        m = MATHS_PATTERN.search(string)  # pylint: disable=invalid-name
        while m:
            lhs, rhs = map(self._check_operands, (m.group("lhs"), m.group("rhs")))
            opr = getop(m.group("op"))
            string = string.replace(m.group(), str(opr(lhs, rhs)))
            m = MATHS_PATTERN.search(string)  # pylint: disable=invalid-name
        return string

    def parse(self, string) -> None:
        self.matches = {d: Dice.from_match(d) for d in DICE_PATTERN.finditer(string)}
        if not self.matches:
            raise ParserError(string)

    def eval(self, func, string):
        self.parse(string)
        string = self._sub_dice(func, string)
        string = self._sub_ops(string)
        return string


def count_dice_attr(attr: Optional[str] = None) -> int:
    if attr:
        return int(attr)
    return 1


def getop(opstring: str) -> Callable:
    ops = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x // y,
    }
    return ops[opstring]


if __name__ == "__main__":
    parser = DiceParser()
    print(parser.eval("roll", "1d20 - 5"))
