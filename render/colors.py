from __future__ import annotations
from numpy import ndarray
from utils.calculations import coerce_in_int, coerce_in_float
from typing import Self
from functools import lru_cache

from dataclasses import dataclass
import dataclasses
import curses
from randomisation.random_seed import RandomSeed

from config import Config
from caparams.ca_params import Caparams


class ColorManager:
    _instance = None
    num_colors = Config.MAX_AGING
    base_color: HslColor | None = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def init_base_color(cls, color: HslColor): 
        cls.base_color = color
        
    @classmethod
    def is_extended(cls) -> bool: return curses.can_change_color()
    @classmethod
    def is_not_extended(cls) -> bool: return not curses.can_change_color()

    @classmethod
    def get_base_color(cls):
        return cls.base_color if cls.base_color is not None else HslColor.random()
    
    @classmethod
    @lru_cache(maxsize=None)
    def num_necessary_colors(cls) -> int:
        max_aging = Config.MAX_AGING
        num_available_colors = curses.COLORS
        num_available_pairs = curses.COLOR_PAIRS
        return min(max_aging, num_available_colors, num_available_pairs)

    @classmethod
    @lru_cache(maxsize=None)
    def colors_list(cls) -> list[int]:
        return list(range(1, cls.num_necessary_colors()))

    @classmethod
    def shuffled_colors(cls) -> list[int]:
        return RandomSeed.rng.permutation(cls.num_necessary_colors()).tolist().tolist()

    @classmethod
    def pick_random_color(cls) -> int:
        return int(RandomSeed.rng.integers(1, cls.num_necessary_colors() + 1))
    
    @classmethod
    def _initialise_extended(cls):
        if cls.is_not_extended: return
        for i in range(1, cls.num_necessary_colors()):
            HslColor.random().curses_init(i)
            curses.init_pair(i, i, -1)

    @classmethod
    def initialise_random_colors(cls):
        curses.start_color()
        curses.use_default_colors()
        cls._initialise_extended()
        for i, color in enumerate(cls.shuffled_colors(), start=1):
            curses.init_pair(i, color, -1)

    @classmethod
    def randomise_colors(cls):
        cls._initialise_extended()
        for i, color in enumerate(cls.shuffled_colors(), start=1):
            _, bg = curses.pair_content(i)
            curses.init_pair(i, color, bg)

    @classmethod
    def randomise_colors_mono(cls):
        picked_color = cls.pick_random_color()
        for color in cls.colors_list():
            _, bg = curses.pair_content(color)
            curses.init_pair(color, picked_color, bg)

    @classmethod
    def random_background(cls, caparams: Caparams, window: curses.window):
        back = cls.pick_random_color()
        for color in cls.colors_list():
            fg, _ = curses.pair_content(color)
            curses.init_pair(color, fg, back)
        window.bkgd(caparams.get_blank_symbol(), curses.color_pair(1))

    @classmethod
    def reset_colors(cls):
        for color in cls.colors_list():
            curses.init_pair(color, -1, -1)

    @classmethod
    def pair_for_aging(cls, aging: int) -> int:
        return min(aging, cls.num_necessary_colors())

    @classmethod
    def gradient(cls) -> bool:
        if ColorManager.is_not_extended(): return False
        base = HslColor.random(saturation= 0.6, lightness=0.6)
        ratio = RandomSeed.rng.uniform(0.5, 60)
        
        for color in cls.colors_list():
            base.shift(hue=color * ratio).curses_init(color)
            curses.init_pair(color, color, -1)

        return True

@dataclass
class HslColor():
    hue: float
    saturation: float
    lightness: float

    def __post_init__(self) -> None:
        self.hue: float = self.hue % 360
        self.saturation: float = coerce_in_float(0.0, 1.0, self.saturation)
        self.lightness: float = coerce_in_float(0.0, 1.0, self.lightness)
    
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

    def shift(
        self,
        hue: float | None = None,
        saturation: float | None = None,
        lightness: float | None = None
    ) -> HslColor:
        h = self.hue + hue if hue is not None else self.hue
        s = self.saturation + saturation if saturation is not None else self.saturation
        l = self.lightness + lightness if lightness is not None else self.lightness
        return HslColor(h, s, l)

    def curses_init(self, color_number): self.to_rgb().curses_init(color_number)

    @classmethod
    def random(cls, 
               hue: float | None = None,
               saturation: float | None = None,
               lightness: float | None = None
              ) -> HslColor:
        return HslColor(
            RandomSeed.rng.uniform(0, 360) if hue is None else hue, 
            RandomSeed.rng.uniform(Config.MIN_SATURATION, Config.MAX_SATURATION) 
            if saturation is None else saturation, 
            RandomSeed.rng.uniform(Config.MIN_LIGHTNESS, Config.MAX_LIGHTNESS) 
            if lightness is None else lightness
        )

@dataclass
class RgbColor():
    red: int
    green: int
    blue: int

    def __post_init__(self) -> None:
        self.red = coerce_in_int(0, 1000, self.red)
        self.green = coerce_in_int(0, 1000, self.green)
        self.blue = coerce_in_int(0, 1000, self.blue)

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

    def curses_init(self, color_number): 
        curses.init_color(color_number, self.red, self.green, self.blue)

    @classmethod
    def random(cls) -> RgbColor:
        return RgbColor(
            int(RandomSeed.rng.integers(0, 1000)), 
            int(RandomSeed.rng.integers(0, 1000)), 
            int(RandomSeed.rng.integers(0, 1000))
        )

    