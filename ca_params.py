from enum import Enum, auto

from cellular_automaton.figure import Figure
from cellular_automaton.rule import Rule


class Caparams():
    def __init__(self, stdscr, 
                 figure: Figure = Figure(),
                 rule: Rule = Rule(),
                 delay: float = 0.1
                 ):
        self.stdscr = stdscr
        self.figure = figure
        self.rule = rule
        self.delay = delay
        self.stuck_behaviour: StuckBehaviour = StuckBehaviour.PAUSE

    def toogle_stuck_behaviour(self):
        self.stuck_behaviour = StuckBehaviour.next(self.stuck_behaviour)

class StuckBehaviour(Enum):
    PAUSE = auto()
    FILL = auto()
    STOP = auto()

    @classmethod
    def next(cls, mode: StuckBehaviour) -> StuckBehaviour:
        members = list(cls)
        return members[(members.index(mode) + 1) % len(members)]