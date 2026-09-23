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
    def figure_parse_contain_type(arg: str) -> Cell:
        return CommonParse._parse_or_raise("contain", FigureParse.validate_contain, arg)

    @staticmethod
    def figure_parse_rect_type(arg: str) -> tuple[int, int]:
        return CommonParse._parse_or_raise("rect", FigureParse.validate_rect, arg)

    @staticmethod
    def rule_parse_type(arg: str) -> Rule:
        return CommonParse._parse_or_raise("rule", RuleParse.validate_rule, arg)

    

    