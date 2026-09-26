from alignment.arrangement import Arrangment
from parsing.render_parse import RenderParse
from alignment.window_calc import Offset
from parsing.utils_parse import UtilsParse
import statistics
from config import Config
from parsing.rule_parse import RuleParse
from cellular_automaton.rule import Rule
from parsing.figure_parse import FigureParse, Cell
import argparse

class CommonParse():

    @staticmethod
    def _parse_or_raise(label: str, fn, *args, **kwargs):
      try:
          return fn(*args, **kwargs)
      except ValueError as e:
          raise argparse.ArgumentTypeError(f"invalid parse {label}: {e}")

    @staticmethod
    def figure_parse_width_type(arg) -> int:
        return CommonParse._parse_or_raise("width", FigureParse.validate_dimension, arg, 
                                           Config.MIN_DIMENSION, Config.MAX_DIMENSION)

    @staticmethod
    def figure_parse_height_type(arg) -> int:
        return CommonParse._parse_or_raise("height", FigureParse.validate_dimension, arg, 
                                           Config.MIN_DIMENSION, Config.MAX_DIMENSION)
    
    @staticmethod
    def figure_parse_contain_type(arg: str) -> Cell:
        return CommonParse._parse_or_raise("contain", FigureParse.validate_contain, arg)

    @staticmethod
    def figure_parse_rect_type(arg: str) -> tuple[int, int]:
        return CommonParse._parse_or_raise("rect", FigureParse.validate_rect, arg)

    @staticmethod
    def figure_parse_fill_type(arg: str) -> float:
        return CommonParse._parse_or_raise("fill", FigureParse.validate_fill, arg)

    @staticmethod
    def rule_parse_type(arg: str) -> Rule:
        return CommonParse._parse_or_raise("rule", RuleParse.validate_rule, arg)

    @staticmethod
    def player_parse_delay_type(arg: str) -> float:
        return CommonParse._parse_or_raise("delay", UtilsParse.parse_float, arg, 0, Config.MAX_DELAY)

    @staticmethod
    def render_parse_offset_type(arg: str) -> Offset:
        return CommonParse._parse_or_raise("offset", RenderParse.parse_offset, arg)

    @staticmethod
    def render_parse_align_type(arg: str) -> Arrangment:
        return CommonParse._parse_or_raise("align", RenderParse.parse_arrangment, arg)



    

    