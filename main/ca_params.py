from __future__ import annotations
from debug import printl

import curses
from enum import Enum, auto

import numpy as np

from cellular_automaton.figure import Figure
from cellular_automaton.rule import Rule
from config import Config
from randomisation.randoms import random_symbols


class Caparams():
    def __init__(self, stdscr: curses.window, 
                 figure: Figure,
                 rule: Rule,
                 delay: float,
                 stuck_behaviour: StuckBehaviour,
                 symbols: str,
                 seed: int
                 ):
        self.stdscr = stdscr
        self.figure = figure
        self.rule = rule
        self.delay = self.fix_delay(delay)
        self.stuck_behaviour: StuckBehaviour = stuck_behaviour
        self.symbols_array = self.build_symbols_array(symbols)
        self.seed = seed

    def toogle_stuck_behaviour(self):
        self.stuck_behaviour = StuckBehaviour.next(self.stuck_behaviour)

    def init_symbols(self, symbols: str):
        self.symbols_array = self.build_symbols_array(symbols=symbols)

    def build_symbols_array(self, symbols: str):
        symbols_list = list(symbols) or [" ", "■"]
        shape = self.rule.aging + 1
        arr = np.full(shape=shape, fill_value=symbols_list[-1], dtype="<U1")
        for i, ch in enumerate(symbols_list[:shape]):
            arr[i] = ch
        return arr

    def increase_delay(self, by: float = 2): self.set_delay(self.delay * by)

    def decrease_delay(self, by: float = 2): self.set_delay(self.delay / by)

    def set_delay(self, candidate: float): self.delay = self.fix_delay(candidate=candidate)

    def fix_delay(self, candidate: float) -> float:
        return (0 if candidate < Config.MIN_DELAY else round(min(max(candidate, 0.01), Config.MAX_DELAY), 2)) if candidate > 0 else Config.MIN_DELAY

    def get_blank_symbol(self):
        return self.symbols_array[0] if len(self.symbols_array) else " "

class StuckBehaviour(Enum):
    PAUSE = auto()
    CONTINUE = auto()
    STOP = auto()

    @classmethod
    def next(cls, mode: StuckBehaviour) -> StuckBehaviour:
        members = list(cls)
        return members[(members.index(mode) + 1) % len(members)]