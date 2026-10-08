from __future__ import annotations
from numpy.typing import NDArray
from caparams.pause import Pause
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
                 pause: Pause,
                 history_size: int,
                 ):
        self.stdscr: curses.window = stdscr
        self.figure: Figure = figure
        self.rule: Rule = rule
        self.delay: int = self._fix_delay(delay)
        self.stuck_behaviour: StuckBehaviour = stuck_behaviour
        self.symbols_array: NDArray = self._build_symbols_array(symbols)
        self.frame: bool = frame
        self.offset: Offset = offset
        self.seed: int = seed
        self.pause: Pause = pause
        self.history_size: int = history_size
        
    def toogle_stuck_behaviour(self):
        self.stuck_behaviour = StuckBehaviour.next(self.stuck_behaviour)

    def get_symbol_by_age(self, age: int): 
        return self.symbols_array[min(age, len(self.symbols_array) - 1)]

    def get_blank_symbol(self) -> str:
        return self.symbols_array[0] if len(self.symbols_array) else Config.BASE_SYMBOLS_LIST[0]

    def get_symbols_string(self) -> str: return "".join(self.symbols_array)

    def increase_delay(self, by: float = 2): 
        self.set_delay(max(int(self.delay * by), Config.MIN_DELAY))

    def decrease_delay(self, by: float = 2): 
        new = 0 if self.delay <= Config.MIN_DELAY else max(int(self.delay / by), Config.MIN_DELAY)
        self.set_delay(new)

    def set_delay(self, candidate: int): self.delay = self._fix_delay(candidate=candidate)

    def _fix_delay(self, candidate: int) -> int: 
        return 0 if candidate < Config.MIN_DELAY else min(candidate, Config.MAX_DELAY)
        
    def frame_toogle(self): self.frame = not self.frame

    def getTermSize(self) -> Size:
        return Size.from_curses_window(self.stdscr)
    def getTermWidth(self) -> int: return self.getTermSize().width
    def getTermHeight(self) -> int: return self.getTermSize().height
    def getFigSize(self) -> Size:
        return self.figure.size()

    def init_symbols(self, symbols: str):
        self.symbols_array = self._build_symbols_array(symbols=symbols)
    
    def _build_symbols_array(self, symbols: str) -> NDArray:
        return np.array(list(symbols) or Config.BASE_SYMBOLS_LIST, dtype="<U1")