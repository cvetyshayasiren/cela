import curses

from main.arg_parser import arg_parser, complete_namespace
import argparse
from main.colors import ColorManager
from randomisation.random_seed import RandomSeed

def initialise():
  args = arg_parser()
  RandomSeed.init(seed = args.seed)
  ColorManager.initialise_random_colors()
  # curses.wrapper(main, args)
  
  