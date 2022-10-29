from __future__ import annotations

import operator
import re
from dataclasses import dataclass
from random import randint
from typing import Callable, Match, Optional

DICE_PATTERN = re.compile(r"(\d*)d(\d+)")
MATHS_PATTERN = re.compile(r"(?P<lhs>\w*)\s*(?P<op>[-+\/*])\s*(?P<rhs>\w*)")


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


class DiceParser:
    def __init__(self):
        self.matches = None

    def parse(self, string):
        self.matches = {d: Dice.from_match(d) for d in DICE_PATTERN.finditer(string)}
        if not self.matches:
            raise ParserError(string)

    def _sub_dice(self, func, string):
        for k, dice in self.matches.items():
            # count = 1 so repeated dice in the same string don't roll the same value
            # e.g., 1d6 + 4 + 1d6 would evaluate both '1d6s' to the same value
            # if count = -1
            string = string.replace(k.group(), str(getattr(Dice, func)(dice)), 1)
        return string

    def _sub_ops(self, string):
        m = MATHS_PATTERN.search(string)  # pylint: disable=invalid-name
        while m:
            try:
                res = getop(m.group("op"))(int(m.group("lhs")), int(m.group("rhs")))
            except ValueError as err:
                raise ParserError(m.group()) from err
            string = string.replace(m.group(), str(res))
            m = MATHS_PATTERN.search(string)  # pylint: disable=invalid-name
        return string

    def safe_eval(self, func, string):
        self.parse(string)
        string = self._sub_dice(func, string)
        print(string)
        string = self._sub_ops(string)
        return int(string)


def count_dice_attr(attr: Optional[str] = None) -> int:
    if attr:
        return int(attr)
    return 1


def getop(opstring: str) -> Callable:
    ops = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
    }
    return ops[opstring]


if __name__ == "__main__":
    parser = DiceParser()
    rolled = parser.safe_eval("roll", "3d6+5 *d20+3d6")
    print(rolled)
