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
        self.show_tips = False

    def init_symbols(self, symbols: str = random_symbols()):
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

    def toogle_tips(self): self.show_tips = not self.show_tips

    def draw(self, paused: bool):
        self.stdscr.erase()
        generation = self.figure.generation
        h, w = self.stdscr.getmaxyx()

        for i, j in np.ndindex(generation.shape):
            if i >= h - 1 or j >= w - 1: continue
            value = generation[i, j]
            self.stdscr.addstr(i, j, self.symbols[value], curses.color_pair(value))

        size_string = f"{self.figure.width}x{self.figure.height}"
        pause_state_string = "paused" if paused else ""
        state_string = f"{size_string} | {pause_state_string} | i - show tips"
        tips_string = (
            f"q - exit\n"
            "p - pause/resume\n"
            "r - randomise field\n"
            "c - randomise color\n"
            "s - randomise symbols\n"
            "(1-9) - add square in center\n"
            "b - blank field"
        )
        number_tips_cols = tips_string.count("\n") + 1
        if(self.show_tips):
            self.stdscr.addstr(h - number_tips_cols, 0, tips_string)
        self.stdscr.addstr(h - 1, 0, state_string[:w - 1])
        self.stdscr.refresh()
        
