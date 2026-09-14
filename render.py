import curses
import random

import numpy as np
from enum import Enum, auto

from ca_params import Caparams
from utils.randoms import random_symbols




class Render():
    def __init__(self, caparams: Caparams):
        self.caparams = caparams
        self.tips_mode: TipsMode = TipsMode.MINI
        self.randomise_colors()

    def randomise_colors(self, fill: bool = False) -> list[int]:
        curses.start_color()
        curses.use_default_colors()
        num_colors = self.caparams.rule.aging + 1
        available_colors = list(range(1, curses.COLORS))
        picked_colors = random.sample(available_colors, min(num_colors, len(available_colors)))
        filling = random.choice(available_colors)
        for i, color in enumerate(picked_colors, start=0):
            if(fill): curses.init_pair(i, color, filling)
            else: curses.init_pair(i, color, -1)

    def random_background(self):
        back = random.randint(1, curses.COLORS)

        for i in list(range(1, curses.COLORS)):
            curses.init_pair(i, curses.COLOR_WHITE, back)
        # self.caparams.stdscr.bkgd(self.caparams.symbols_array[0], curses.color_pair(back))

    def reset_colors(self):
        for i in list(range(1, curses.COLORS)):
            curses.init_pair(i, curses.COLOR_WHITE, -1)
        

    def toogle_tips(self): self.tips_mode = TipsMode.next(self.tips_mode)

    def draw(self, paused: bool):
        self.caparams.stdscr.erase()
        generation = self.caparams.figure.generation
        h, w = self.caparams.stdscr.getmaxyx()

        for i, j in np.ndindex(generation.shape):
            if i >= h or j >= w - 1: continue
            value = generation[i, j]
            self.caparams.stdscr.addstr(i, j, 
                                        self.caparams.symbols_array[value], 
                                        curses.color_pair(value))
        self.draw_tips(paused = paused, h = h, w = w)

        self.caparams.stdscr.refresh()

    def draw_tips(self, paused: bool, h: int, w: int):
        if(self.tips_mode == TipsMode.HIDDEN): return

        size_string = f"{self.caparams.figure.width}x{self.caparams.figure.height}"
        pause_state_string = "paused" if paused else ""
        state_string = f"{size_string} | {pause_state_string} | i - show tips | delay {self.caparams.delay}"
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

        if(self.tips_mode == TipsMode.FULL):
            self.caparams.stdscr.addstr(h - number_tips_cols, 0, tips_string)
            self.caparams.stdscr.addstr(h - 1, 0, state_string[:w - 1])
        else:
            self.caparams.stdscr.addstr(h - 1, 0, state_string[:w - 1])


class TipsMode(Enum):
    HIDDEN = auto()
    MINI = auto()
    FULL = auto()

    @classmethod
    def next(cls, mode: TipsMode) -> TipsMode:
        members = list(cls)
        return members[(members.index(mode) + 1) % len(members)]