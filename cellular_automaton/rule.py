import re
from typing import Set

class Rule:
    game_of_life = "B3/S23"
    game_of_fly = "B2/S0345/10"

    def __init__(self, 
                 born: Set[int] = {3}, 
                 survive: Set[int] = {2,3}, 
                 aging: int = 1
                 ):
        self.born: Set[int] = born
        self.survive: Set[int] = survive
        self.aging: int = aging
        self.string = self.to_string()

    def to_string(self) -> str:
        b = "B" + "".join(str(b) for b in sorted(self.born))
        s = "S" + "".join(str(s) for s in sorted(self.survive))
        return f"{b}/{s}/{self.aging}"

    @staticmethod
    def from_string(string: str) -> "Rule":
        string = string.upper()
        parts = string.split('/')
        if len(parts) not in (2, 3):
            raise ValueError("expected B.../S...[/aging]")

        b_part, s_part = parts[0], parts[1]
        aging_part = parts[2] if len(parts) == 3 else "1"

        if not b_part.startswith("B") or not s_part.startswith("S"):
            raise ValueError("expected B.../S...[/aging]")

        def parse_digits(part: str) -> set[int]:
            digits = part[1:]
            if not digits or not digits.isdigit():
                raise ValueError("invalid digits")
            return {int(c) for c in digits}

        if not aging_part.isdigit() or int(aging_part) < 1:
            raise ValueError("invalid aging")

        return Rule(
            born=parse_digits(b_part),
            survive=parse_digits(s_part),
            aging=int(aging_part),
        )


        
        
