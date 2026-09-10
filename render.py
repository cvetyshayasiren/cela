import curses
import random

import numpy as np

from cellular_automaton.figure import Figure
from utils.randoms import random_symbols


class Render():
    def __init__(self, stdscr, figure: Figure, aging: int, symbols: str = random_symbols()):
        self.stdscr = stdscr
        self.figure = figure
        self.aging = aging
        self.symbols = self.init_symbols(symbols=symbols)
        self.init_colors()

    def init_symbols(self, symbols: str):
        symbols = list(symbols) or [" ", "■"]
        shape = self.aging + 1
        arr = np.full(shape=shape, fill_value=symbols[-1], dtype="<U1")
        for i, ch in enumerate(symbols[:shape]):
            arr[i] = ch
        return arr

    def init_colors(self) -> list[int]:
        curses.start_color()
        curses.use_default_colors()
        num_colors = self.aging + 1
        available_colors = list(range(1, curses.COLORS))
        picked_colors = random.sample(available_colors, min(num_colors, len(available_colors)))
        for i, color in enumerate(picked_colors, start=0):
            curses.init_pair(i, color, -1)

    def draw(self):
        self.stdscr.erase()
        generation = self.figure.generation
        h, w = self.stdscr.getmaxyx()

        for i, j in np.ndindex(generation.shape):
            if i >= h - 1 or j >= w - 1: continue
            value = generation[i, j]
            self.stdscr.addstr(i, j, self.symbols[value], curses.color_pair(value))
        self.stdscr.addstr(h - 1, 0, f"{self.figure.width}x{self.figure.height}")
        self.stdscr.refresh()
        
