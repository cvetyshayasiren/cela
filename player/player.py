import caparams
from player.history import PlayerHistory
from parsing.arg_parser import args_to_params
from parsing.arg_builder import ArgBuilder
import curses
import numpy as np

from caparams.ca_params import Caparams
from caparams.stuck_behaviour import StuckBehaviour
from debug import printd, printl
from render.colors import ColorManager
from render.render import Render
from randomisation.randoms import random_symbols

class Player:

    def __init__(self, caparams: Caparams):
        self.caparams: Caparams = caparams
        self.render: Render = Render(caparams=caparams)
        self.is_playing: bool = False
        self.dragging: bool = False
        self.init_mouse()
        self.output: str = ""
        
        self.history: PlayerHistory | None = self._init_history(caparams.history_size)

    def play(self):
        if self.is_playing: return
        self.is_playing = True

        while(self.is_playing == True):
            self.caparams.stdscr.timeout(self.caparams.delay)
            self.button_handler()
            if self.caparams.paused: continue
            old_generation = self.caparams.figure.generation
            next = self.caparams.figure.next(rule=self.caparams.rule)
            new_generation = self.caparams.figure.generation
            self.save_history(old_generation)
            equal = np.array_equal(old_generation, new_generation)
            if equal: self.stuck_behaviour()
            self.draw()

    def step(self):
        pass

    def stuck_behaviour(self):
        match self.caparams.stuck_behaviour:
            case StuckBehaviour.PAUSE:
                self.paused = True
            case StuckBehaviour.CONTINUE:
                self.caparams.figure.fill_full_random()
            case StuckBehaviour.STOP:
                self.stop()
    

    def stop(self):
        self.is_playing = False

    def button_handler(self):
        key = self.caparams.stdscr.getch()
        self.mouse_handler(key)

        if key == ord('q') or key == 27:
            self.stop()

        elif key == ord('p'):
            self.caparams.pause_toogle()

        elif key == curses.KEY_RIGHT or key == ord('n'):
            if(self.caparams.is_paused()):
                self.caparams.figure.next(self.caparams.rule)
                self.save_history()

        elif key == curses.KEY_UP and self.render.is_no_need_tips_control(): self.caparams.increase_delay(by=2)

        elif key == curses.KEY_DOWN and self.render.is_no_need_tips_control(): self.caparams.decrease_delay(by=2)

        elif key == curses.KEY_UP and self.render.is_need_tips_control(): self.render.move_tips_up()

        elif key == curses.KEY_DOWN and self.render.is_need_tips_control(): self.render.move_tips_down()

        elif key == curses.KEY_LEFT and self.history is not None and len(self.history.history) > 0:
            self.caparams.pause_toogle(value=True)
            self.caparams.figure.generation = self.history.take()

        elif key == ord('r'):
            self.caparams.figure.fill_full_random()

        elif ord('0') <= key <= ord('9'): 
            digit = key - ord('0')
            self.caparams.figure.fill_random_range(low=digit/10, high=(digit+1)/10)

        elif key == ord('b'):
            self.caparams.figure.blank_field()

        elif key == ord('s'):
            self.caparams.init_symbols(symbols=random_symbols())

        elif key == ord('.'):
            ColorManager.randomise_colors()

        elif key == ord(','):
            ColorManager.random_background(caparams=self.caparams)

        elif key == ord('/'):
            ColorManager.reset_colors()

        elif key == ord('i'):
            self.render.toogle_tips()

        elif key == ord('`'):
            self.caparams.pause()
            self.output = ArgBuilder.build_args_string(caparams=self.caparams)
            self.stop()

        elif key == ord('f'):
            self.render.frame_toogle()

        self.draw_if_paused()
        
    def mouse_handler(self, key):
        if key != curses.KEY_MOUSE: return
        try:
            _, x, y, _, bstate = curses.getmouse()
            if bstate & curses.BUTTON1_CLICKED:
                self.caparams.figure.toogle_cell(x = x, y = y)

            elif bstate & curses.BUTTON1_PRESSED and not self.dragging:
                self.dragging = True
                curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
                self.caparams.figure.contain_rect(x=x, y=y)

            elif bstate & curses.BUTTON1_RELEASED and self.dragging:
                self.dragging = False
                curses.mousemask(curses.ALL_MOUSE_EVENTS)
        except curses.error:
            pass

    def draw(self):
        self.render.draw()
        
    def draw_if_paused(self):
        if(self.caparams.paused): self.draw()

    def init_mouse(self):
        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        self.caparams.stdscr.keypad(True)

    def _init_history(self, history_size: int) -> PlayerHistory | None:
        return PlayerHistory(history_size) if history_size > 0 else None

    def _is_need_save_on_history(self) -> bool:
        return self.history is not None

    def save_history(self, generation: np.ndarray):
        if self.history is not None:
            self.history.save(generation)

    