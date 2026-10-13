from __future__ import annotations
from typing import Self

from dataclasses import dataclass
import dataclasses
import curses
from randomisation.random_seed import RandomSeed

from config import Config
from caparams.ca_params import Caparams


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
    def num_available_pair(cls):
        return curses.COLOR_PAIRS - 1

    @classmethod
    def list_available_colors(cls):
        return list(range(1, curses.COLORS))

    @classmethod
    def num_necessary_colors(cls):
        return min(cls.num_colors, cls.num_available_colors(), cls.num_available_pair())

    @classmethod
    def initialise_random_colors(cls):
        curses.start_color()
        curses.use_default_colors()
        picked_colors = RandomSeed.rng.choice(cls.list_available_colors(), cls.num_necessary_colors(), replace=False)
        for i, color in enumerate(picked_colors, start=1):
            curses.init_pair(i, color, -1)

    @classmethod
    def randomise_colors(cls):
        picked_colors = RandomSeed.rng.choice(cls.list_available_colors(), cls.num_necessary_colors(), replace=False)
        for i, color in enumerate(picked_colors, start=1):
            _, bg = curses.pair_content(i)
            curses.init_pair(i, color, bg)

    @classmethod
    def randomise_colors_mono(cls):
        picked_color = RandomSeed.rng.integers(1, cls.num_available_colors() + 1)
        for i in range(1, cls.num_necessary_colors() + 1):
            _, bg = curses.pair_content(i)
            curses.init_pair(i, picked_color, bg)

    @classmethod
    def random_background(cls, caparams: Caparams, window: curses.window):
        back = RandomSeed.rng.integers(1, cls.num_available_colors() + 1)
        for i in range(1, cls.num_necessary_colors() + 1):
            fg, _ = curses.pair_content(i)
            curses.init_pair(i, fg, back)
        window.bkgd(caparams.get_blank_symbol(), curses.color_pair(1))

    @classmethod
    def reset_colors(cls):
        for i in range(1, cls.num_necessary_colors() + 1):
            curses.init_pair(i, curses.COLOR_WHITE, -1)

    @classmethod
    def pair_for_aging(cls, aging: int) -> int:
        return min(aging, cls.num_necessary_colors())

    @classmethod
    def test_colors(cls):
        steps = cls.num_necessary_colors() + 1
        left_border = RandomSeed.rng.integers(1, 361)
        config_max_gradient_width = 360
        right_border = RandomSeed.rng.integers(1, config_max_gradient_width + 1)
        border_diff = ((360 + right_border - left_border) % 360) / steps
        
        for i in range(steps):
            h = (left_border + (border_diff * i)) % 360
            rgb = HslColor(h, 1.0, 0.5).to_rgb()
            col_n = i + steps
            curses.init_color(col_n, rgb.red, rgb.green, rgb.blue)
            curses.init_pair(i, col_n, -1)

@dataclass
class HslColor():
    hue: float
    saturation: float
    lightness: float

    def __post_init__(self) -> None:
        self.hue = self.hue % 360
        self.saturation = max(0.0, min(1.0, self.saturation))
        self.lightness = max(0.0, min(1.0, self.lightness))
    
    def to_rgb(self) -> RgbColor:
        c = (1 - abs(2 * self.lightness - 1)) * self.saturation
        x = c * (1 - abs((self.hue / 60) % 2 - 1))
        m = self.lightness - c / 2
    
        if   self.hue < 60:  r, g, b = c, x, 0
        elif self.hue < 120: r, g, b = x, c, 0
        elif self.hue < 180: r, g, b = 0, c, x
        elif self.hue < 240: r, g, b = 0, x, c
        elif self.hue < 300: r, g, b = x, 0, c
        else:                r, g, b = c, 0, x

        return RgbColor(int((r + m) * 1000), int((g + m) * 1000), int((b + m) * 1000))

@dataclass
class RgbColor():
    red: int
    green: int
    blue: int

    def __post_init__(self) -> None:
        self.red = max(0, min(1000, self.red))
        self.green = max(0, min(1000, self.green))
        self.blue = max(0, min(1000, self.blue))

    def to_hsl(self) -> HslColor:
        r: float = self.red / 1000
        g: float = self.green / 1000 
        b: float = self.blue / 1000
        mx = max(r, g, b)
        mn = min(r, g, b)
        l = (mx + mn) / 2
        d = mx - mn

        if d == 0:
            return HslColor(0.0, 0.0, l)

        s = d / (1 - abs(2 * l - 1))

        if mx == r:
            h = 60 * (((g - b) / d) % 6)
        elif mx == g:
            h = 60 * ((b - r) / d + 2)
        else:
            h = 60 * ((r - g) / d + 4)

        return HslColor(h, s, l)
    