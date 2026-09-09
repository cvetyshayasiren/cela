from typing import Set

class Rule:

    def __init__(self, born: Set[int], survive: Set[int], aging: int):
        self.born: Set[int] = born
        self.survive: Set[int] = survive
        self.aging: int = aging

    def validate(self) -> str:
        if not all(0 <= b <= 8 for b in self.born):
            return "wrong born"

        if not all(0 <= s <= 8 for s in self.survive):
            return "wrong survive"

        if not self.aging >= 1:
            return "wrong aging"
        return ""
        
        
