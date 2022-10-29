from __future__ import annotations

from dataclasses import dataclass
from random import randint
from typing import Match, Optional


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


def count_dice_attr(attr: Optional[str] = None) -> int:
    if attr:
        return int(attr)
    return 1
