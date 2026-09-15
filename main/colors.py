import curses
import random

from config import Config


class ColorManager:
    curses.start_color()
    curses.use_default_colors()
    num_colors = Config.MAX_AGING
    num_available_colors = curses.COLORS - 1
    list_available_colors = list(range(1, curses.COLORS))
    num_necessary_colors = min(num_colors, num_available_colors)

    @classmethod
    def initialise_random_colors(cls):
        curses.start_color()
        curses.use_default_colors()
        picked_colors = random.sample(cls.list_available_colors, cls.num_necessary_colors)
        for i, color in enumerate(picked_colors, start=0):
            curses.init_pair(i, color, -1)

    @classmethod
    def randomise_colors(cls):
        picked_colors = picked_colors = random.sample(cls.list_available_colors, cls.num_necessary_colors)
        for i, color in enumerate(picked_colors, start=0):
            _, bg = curses.pair_content(i)
            curses.init_pair(i, color, bg)

    @classmethod
    def random_background(cls, stdscr: curses.window, blank_symbol: str):
        back = random.randint(1, curses.COLORS)
        for i in range(0, cls.num_necessary_colors):
            fg, _ = curses.pair_content(i)
            curses.init_pair(i, fg, back)
        stdscr.bkgd(blank_symbol, curses.color_pair(1))

    @classmethod
    def reset_colors(cls):
        for i in list(range(1, cls.num_necessary_colors)):
            curses.init_pair(i, curses.COLOR_WHITE, -1)
