from __future__ import annotations
from render.tips import Tips, TipsMode
from alignment.window_calc import Size
from render.colors import ColorManager
import curses

import numpy as np
from enum import Enum, auto

from main.ca_params import Caparams


class Render():
    def __init__(self, caparams: Caparams):
        self.caparams = caparams
        self.tips: Tips = Tips(self.caparams)
        self.ca_win: curses.window = curses.newwin(
            self.caparams.figure.height, self.caparams.figure.width,
            self.caparams.offset.y, self.caparams.offset.x
        )

    def draw(self):
        self.draw_win()
        self.draw_frame()
        self.tips.draw_tips(self.ca_win)
        self.ca_win.noutrefresh()
        curses.doupdate()

    def draw_win(self):
        generation = self.caparams.figure.generation
        h, w = self.ca_win.getmaxyx()

        for i, j in np.ndindex(generation.shape):
            if i >= h or j >= w - 1: continue
            value = generation[i, j]
            self.ca_win.addstr(i, j, 
                                        self.caparams.get_symbol(age=value),
                                        curses.color_pair(ColorManager.pair_for_aging(value))
                                       )

    def draw_frame(self):
        if self.caparams.frame:
            self.ca_win.box()

    def frame_toogle(self):
        self.caparams.frame_toogle()
        self.caparams.stdscr.erase()
        self.draw()

    def toogle_tips(self):
        mode = self.tips.toogle_tips()
        if mode == TipsMode.HIDDEN:
            self._reset_screen()
    
    def move_tips_down(self):
        self.tips.move_down()

    def move_tips_up(self):
        self.tips.move_up()

    def _reset_screen(self):
        self.ca_win.erase()
        self.draw()

    def is_need_tips_control(self) -> bool:
        return self.tips.tips_mode == TipsMode.FULL

    def is_no_need_tips_control(self) -> bool:
        return not self.is_need_tips_control()
        