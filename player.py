import curses
from enum import Enum, auto
import time

from ca_params import Caparams
from cellular_automaton.figure import Figure
from cellular_automaton.rule import Rule
from render import Render
from utils.randoms import random_symbols

class Player:

    def __init__(self, caparams: Caparams):
        self.caparams = caparams
        self.render = Render(caparams=caparams)
        self.is_playing: bool = False
        self.paused = False

    def play(self):
        self.is_playing = True
        self.caparams.stdscr.timeout(int(self.delay * 1000))

        while(self.is_playing == True):
            self.button_handler()
            if self.paused: continue
            next = self.caparams.figure.next(rule=self.rule)
            if not next: self.stuck_behaviour()
            self.draw()

    def stop(self):
        self.is_playing = False

    def pause_toogle(self):
        self.paused = not self.paused
        self.draw_if_paused()

    def button_handler(self):
        key = self.stdscr.getch()

        if key == ord('q') or key == 27:
            self.stop()
        elif key == ord('p'):
            self.pause_toogle()
        elif key == curses.KEY_RIGHT or key == ord('n'):
            if(self.paused):
                self.figure.next(self.rule)
                self.draw_if_paused()
        elif key == ord('r'):
            self.figure.fill_random()
            self.draw_if_paused()
        elif ord('1') <= key <= ord('9'): 
            digit = key - ord('0')
            self.figure.contain_rect_in_center(digit, digit)
            self.draw_if_paused()
        elif key == ord('b'):
            self.figure.blank_field()
            self.draw_if_paused()

        elif key == curses.KEY_MOUSE:
            _, x, y, _, bstate = curses.getmouse()
            self.figure.contain_rect(x = x, y = y)
            self.draw_if_paused()

        elif key == ord('s'):
            self.render.symbols = self.render.init_symbols(symbols=random_symbols())
            self.draw_if_paused()

        elif key == ord('c'):
            self.render.init_colors(background=False)
            self.draw_if_paused()

        elif key == ord('i'):
            self.render.toogle_tips()
            self.draw_if_paused()

        elif key == ord('/'):
            self.render.init_colors(background=True)
            self.stdscr.bkgd(" ", curses.color_pair(4))

    def draw(self):
        self.render.draw(paused=self.paused)
        
    def draw_if_paused(self):
        if(self.paused): self.draw()

    def stuck_behaviour(self):
        self.caparams.figure.fill_full_random()
    