import curses
import random

from config import Config
from main.ca_params import Caparams


class ColorManager:
    _instance = None
    num_colors = Config.MAX_AGING

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def num_available_colors(cls):
        return curses.COLORS - 1

    @classmethod
    def list_available_colors(cls):
        return list(range(1, curses.COLORS))

    @classmethod
    def num_necessary_colors(cls):
        return min(cls.num_colors, cls.num_available_colors())

    @classmethod
    def initialise_random_colors(cls):
        curses.start_color()
        curses.use_default_colors()
        picked_colors = random.sample(cls.list_available_colors(), cls.num_necessary_colors())
        for i, color in enumerate(picked_colors, start=1):
            curses.init_pair(i, color, -1)

    @classmethod
    def randomise_colors(cls):
        picked_colors = picked_colors = random.sample(cls.list_available_colors(), cls.num_necessary_colors())
        for i, color in enumerate(picked_colors, start=1):
            _, bg = curses.pair_content(i)
            curses.init_pair(i, color, bg)

    @classmethod
    def random_background(cls, caparams: Caparams):
        back = random.randint(1, cls.num_available_colors())
        for i in range(0, cls.num_necessary_colors()):
            fg, _ = curses.pair_content(i)
            curses.init_pair(i, fg, back)
        caparams.stdscr.bkgd(caparams.get_blank_symbol(), curses.color_pair(1))

    @classmethod
    def reset_colors(cls):
        for i in range(1, cls.num_necessary_colors()):
            curses.init_pair(i, curses.COLOR_WHITE, -1)
