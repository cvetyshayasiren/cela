from __future__ import annotations
import re
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
    base_color: HslColor | None = None
    bg: int = -1

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
    def get_base_color(cls) -> HslColor:
        return cls.base_color if cls.base_color is not None else HslColor.random()
    
    @classmethod
    def inject_base_pair(cls): cls.get_base_color().curses_init_pair(1, cls.bg)

    @classmethod
    def set_bg(cls, bg: int):
        if bg > curses.COLORS: return
        cls.bg = bg
    
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
        return RandomSeed.rng.permutation(cls.num_necessary_colors()).tolist()

    @classmethod
    def pick_random_color(cls) -> int:
        return int(RandomSeed.rng.integers(1, cls.num_necessary_colors() + 1))

    @classmethod
    def initialise_random_colors(cls):
        curses.start_color()
        curses.use_default_colors()
        cls.randomise_colors()

    @classmethod
    def randomise_colors(cls):
        if cls.is_extended():
            cls.inject_base_pair()
            for color_num in cls.colors_list()[1:]:
                HslColor.random().curses_init_pair(color_number=color_num, bg=cls.bg)
        else:
            for i, color in enumerate(cls.shuffled_colors(), start=1):
                curses.init_pair(i, color, cls.bg)

    @classmethod
    def randomise_colors_mono(cls):
        cls.set_bg(-1)
        if cls.is_extended():
            cls.inject_base_pair()
        else:
            random_color = cls.pick_random_color()
            curses.init_pair(1, random_color, cls.bg)
            
        fg, _ = curses.pair_content(1)
        for color_num in cls.colors_list()[1:]:
            curses.init_pair(color_num, fg, cls.bg)

    @classmethod
    def random_background(cls, caparams: Caparams, window: curses.window):
        if cls.is_extended():
            HslColor.random(
                saturation=Config.BG_SATURATION, 
                lightness=Config.BG_LIGHTNESS
            ).curses_init_color(0)
            cls.bg = 0
        else:
            cls.bg = cls.pick_random_color()
        
        for color in cls.colors_list():
            fg, _ = curses.pair_content(color)
            curses.init_pair(color, fg, cls.bg)
        window.bkgd(caparams.get_blank_symbol(), curses.color_pair(1))

    @classmethod
    def reset_colors(cls):
        cls.set_bg(-1)
        for color in cls.colors_list():
            curses.init_pair(color, -1, cls.bg)

    @classmethod
    def pair_for_aging(cls, aging: int) -> int:
        return min(aging, cls.num_necessary_colors())

    @classmethod
    def gradient(cls) -> bool:
        if ColorManager.is_not_extended(): return False
        base = cls.get_base_color()
        gradient_step = RandomSeed.rng.uniform(Config.MIN_GRADIENT_STEP, Config.MAX_GRADIENT_STEP)
        base.curses_init_pair(1, bg = cls.bg)
        
        for color in cls.colors_list()[1:]:
            base.shift(hue = color+gradient_step).curses_init_pair(color, bg = cls.bg)

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

    def copy(
        self,
        hue: float | None = None,
        saturation: float | None = None,
        lightness: float | None = None
    ) -> HslColor:
        h = hue if hue is not None else self.hue
        s = saturation if saturation is not None else self.saturation
        l = lightness if lightness is not None else self.lightness
        return HslColor(h, s, l)
    
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

    def curses_init_color(self, color_number): self.to_rgb().curses_init_color(color_number)
    def curses_init_pair(self, color_number: int, bg: int = -1): 
        self.to_rgb().curses_init_pair(color_number, bg)

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

    def curses_init_color(self, color_number: int): 
        curses.init_color(color_number, self.red, self.green, self.blue)

    def curses_init_pair(self, color_number: int, bg: int = -1):
        self.curses_init_color(color_number=color_number)
        curses.init_pair(color_number, color_number, bg)

    @classmethod
    def random(cls) -> RgbColor:
        return RgbColor(
            int(RandomSeed.rng.integers(0, 1000)), 
            int(RandomSeed.rng.integers(0, 1000)), 
            int(RandomSeed.rng.integers(0, 1000))
        )

    