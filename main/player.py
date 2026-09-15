import curses

from main.ca_params import Caparams
from debug import printd, printl
from main.colors import ColorManager
from main.render import Render
from utils.randoms import random_symbols

class Player:

    def __init__(self, caparams: Caparams):
        self.caparams = caparams
        self.render = Render(caparams=caparams)
        self.is_playing: bool = False
        self.paused = False
        self.dragging = False
        self.init_mouse()


    def play(self):
        if self.is_playing: return
        self.is_playing = True

        while(self.is_playing == True):
            self.caparams.stdscr.timeout(int(self.caparams.delay * 1000))
            self.button_handler()
            if self.paused: continue
            next = self.caparams.figure.next(rule=self.caparams.rule)
            if not next: self.stuck_behaviour()
            self.draw()

    def stop(self):
        self.is_playing = False

    def pause_toogle(self):
        self.paused = not self.paused
        self.draw_if_paused()

    def button_handler(self):
        key = self.caparams.stdscr.getch()
        self.mouse_handler(key)

        if key == ord('q') or key == 27:
            self.stop()

        elif key == ord('p'):
            self.pause_toogle()

        elif key == curses.KEY_RIGHT or key == ord('n'):
            if(self.paused):
                self.caparams.figure.next(self.caparams.rule)
                self.draw_if_paused()

        elif key == curses.KEY_UP: self.caparams.increase_delay(by=2)

        elif key == curses.KEY_DOWN: self.caparams.decrease_delay(by=2)

        elif key == ord('r'):
            self.caparams.figure.fill_random()
            self.draw_if_paused()

        elif ord('1') <= key <= ord('9'): 
            digit = key - ord('0')
            self.caparams.figure.contain_rect_in_center(digit, digit)
            self.draw_if_paused()

        elif key == ord('b'):
            self.caparams.figure.blank_field()
            self.draw_if_paused()

        elif key == ord('s'):
            self.caparams.init_symbols(symbols=random_symbols())
            self.draw_if_paused()

        elif key == ord('.'):
            ColorManager.randomise_colors()
            self.draw_if_paused()

        elif key == ord(','):
            ColorManager.random_background(caparams=self.caparams)
            self.draw_if_paused()

        elif key == ord('/'):
            ColorManager.reset_colors()
            self.draw_if_paused()

        elif key == ord('i'):
            self.render.toogle_tips()
            self.draw_if_paused()



    def mouse_handler(self, key):
        if key != curses.KEY_MOUSE: return
        try:
            _, x, y, _, bstate = curses.getmouse()
            if bstate & curses.BUTTON1_CLICKED:
                self.caparams.figure.contain_dot(x = x, y = y)
                self.draw_if_paused()

            elif bstate & curses.BUTTON1_PRESSED and not self.dragging:
                self.dragging = True
                curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
                self.caparams.figure.contain_rect(x=x, y=y)
                self.draw_if_paused()

            elif bstate & curses.BUTTON1_RELEASED and self.dragging:
                self.dragging = False
                curses.mousemask(curses.ALL_MOUSE_EVENTS)
        except curses.error:
            pass

    def draw(self):
        self.render.draw(paused=self.paused)
        
    def draw_if_paused(self):
        if(self.paused): self.draw()

    def stuck_behaviour(self):
        self.caparams.figure.fill_full_random()

    def init_mouse(self):
        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        self.caparams.stdscr.keypad(True)
    