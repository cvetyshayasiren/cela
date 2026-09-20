from dataclasses import dataclass, field


from config import Config
import re
from typing import Set, ClassVar

@dataclass(slots = True)
class Rule:
    born: Set[int] = field(default_factory=lambda: {3})
    survive: Set[int] = field(default_factory=lambda: {2, 3})
    aging: int = 1
    string: str = field(init=False)

    game_of_life: ClassVar[str] = "B3/S23"
    game_of_fly: ClassVar[str] = "B2/S0345/10"

    def __post_init__(self): self.string = self.to_string()

    def to_string(self) -> str:
        b = "B" + "".join(str(b) for b in sorted(self.born))
        s = "S" + "".join(str(s) for s in sorted(self.survive))
        return f"{b}/{s}/{self.aging}"


        
        
