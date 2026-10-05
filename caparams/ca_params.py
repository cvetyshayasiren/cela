from __future__ import annotations
from caparams.stuck_behaviour import StuckBehaviour
from alignment.window_calc import Offset, Size
from debug import printl


import curses

import numpy as np

from cellular_automaton.figure import Figure
from cellular_automaton.rule import Rule
from config import Config
from randomisation.randoms import random_symbols


class Caparams():
    def __init__(self, stdscr: curses.window, 
                 figure: Figure,
                 rule: Rule,
                 delay: int,
                 stuck_behaviour: StuckBehaviour,
                 symbols: str,
                 frame: bool,
                 offset: Offset,
                 seed: int,
                 paused: bool,
                 history_size: int
                 ):
        self.stdscr = stdscr
        self.figure = figure
        self.rule = rule
        self.delay = self.fix_delay(delay)
        self.stuck_behaviour: StuckBehaviour = stuck_behaviour
        self.symbols_array = self.build_symbols_array(symbols)
        self.frame = frame
        self.offset = offset
        self.seed = seed
        self.paused = paused
        self.history_size = history_size

    def toogle_stuck_behaviour(self):
        self.stuck_behaviour = StuckBehaviour.next(self.stuck_behaviour)

    def init_symbols(self, symbols: str):
        self.symbols_array = self.build_symbols_array(symbols=symbols)

    def build_symbols_array(self, symbols: str):
        return np.array(list(symbols) or [" ", "■"], dtype="<U1")

    def get_symbol(self, age: int): 
        return self.symbols_array[min(age, len(self.symbols_array) - 1)]

    def get_blank_symbol(self):
        return self.symbols_array[0] if len(self.symbols_array) else " "

    def get_symbols_string(self) -> str: return "".join(self.symbols_array)

    def increase_delay(self, by: float = 2): 
        self.set_delay(max(int(self.delay * by), Config.MIN_DELAY))

    def decrease_delay(self, by: float = 2): 
        new = 0 if self.delay <= Config.MIN_DELAY else max(int(self.delay / by), Config.MIN_DELAY)
        self.set_delay(new)

    def set_delay(self, candidate: int): self.delay = self.fix_delay(candidate=candidate)

    def fix_delay(self, candidate: int) -> int: 
        return 0 if candidate < Config.MIN_DELAY else min(candidate, Config.MAX_DELAY)
        

    def is_paused(self) -> bool: return self.paused
    def is_not_paused(self) -> bool: return not self.paused
    
    def pause(self): self.pause_toogle(True)
    def unpause(self): self.pause_toogle(False)
    def pause_toogle(self, value: bool | None = None):
        if value is not None:
            self.paused = value
        else:
            self.paused = not self.paused

    def frame_toogle(self): self.frame = not self.frame

    def getTermSize(self) -> Size:
        return Size.from_curses_window(self.stdscr)
    def getTermWidth(self) -> int: return self.getTermSize().width
    def getTermHeight(self) -> int: return self.getTermSize().height
    def getFigSize(self) -> Size:
        return self.figure.size()