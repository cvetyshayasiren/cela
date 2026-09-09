import re
from typing import Set

class Rule:

    def __init__(self, born: Set[int], survive: Set[int], aging: int):
        self.born: Set[int] = born
        self.survive: Set[int] = survive
        self.aging: int = aging

    @staticmethod
    def from_string(string: str) -> Rule:
        b_part, s_part, a_part = string.split('/')
        born = {int(c) for c in re.findall(r'\d', b_part)}
        survive = {int(c) for c in re.findall(r'\d', s_part)}
        aging = int(a_part)
        return Rule(born=born, survive=survive, aging=aging)

    def validate(self) -> str:
        if not all(0 <= b <= 8 for b in self.born):
            return "wrong born"

        if not all(0 <= s <= 8 for s in self.survive):
            return "wrong survive"

        if not self.aging >= 1:
            return "wrong aging"
        return ""


        
        
