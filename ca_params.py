from enum import Enum, auto

import numpy as np

from cellular_automaton.figure import Figure
from cellular_automaton.rule import Rule
from utils.randoms import random_symbols


class Caparams():
    def __init__(self, stdscr, 
                 figure: Figure = Figure(),
                 rule: Rule = Rule(),
                 delay: float = 0.1,
                 symbols: str = random_symbols()
                 ):
        self.stdscr = stdscr
        self.figure = figure
        self.rule = rule
        self.delay = delay
        self.stuck_behaviour: StuckBehaviour = StuckBehaviour.PAUSE
        self.symbols_array = self.build_symbols_array(symbols)

    def toogle_stuck_behaviour(self):
        self.stuck_behaviour = StuckBehaviour.next(self.stuck_behaviour)

    def init_symbols(self, symbols: str = random_symbols()):
        self.symbols_array = self.build_symbols_array(symbols=symbols)

    def build_symbols_array(self, symbols: str = random_symbols()):
        symbols = list(symbols) or [" ", "■"]
        shape = self.aging + 1
        arr = np.full(shape=shape, fill_value=symbols[-1], dtype="<U1")
        for i, ch in enumerate(symbols[:shape]):
            arr[i] = ch
        return arr

class StuckBehaviour(Enum):
    PAUSE = auto()
    FILL = auto()
    STOP = auto()

    @classmethod
    def next(cls, mode: StuckBehaviour) -> StuckBehaviour:
        members = list(cls)
        return members[(members.index(mode) + 1) % len(members)]