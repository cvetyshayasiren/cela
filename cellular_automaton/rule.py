from config import Config
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


        
        
