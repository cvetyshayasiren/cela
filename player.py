import curses
import time

from cellular_automaton.figure import Figure
from cellular_automaton.rule import Rule
from render import Render
from utils.randoms import random_symbols

class Player:

    def __init__(self, stdscr,
                 figure: Figure = Figure(), 
                 rule: Rule = Rule(),
                 delay: float = 0.1
                 ):
        self.stdscr = stdscr
        self.figure = figure
        self.rule = rule
        self.delay = delay
        self.render = Render(stdscr, figure, rule.aging)
        self.is_playing: bool = False
        self.paused = False

    def play(self):
        self.is_playing = True
        self.stdscr.timeout(int(self.delay * 1000))

        while(self.is_playing == True):
            self.button_handler()
            if self.paused: continue
            self.figure.next(rule=self.rule)
            self.draw()

    def stop(self):
        self.is_playing = False
        print("lal")

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
            self.render.init_colors()
            self.draw_if_paused()

        elif key == ord('i'):
            self.render.toogle_tips()
            self.draw_if_paused()

    def draw(self):
        self.render.draw(paused=self.paused)
        
    def draw_if_paused(self):
        if(self.paused): self.draw()


    