import argparse
import curses

from main.arg_parser import arg_parser, args_to_params, complete_namespace
from main.player import Player
from main.colors import ColorManager
from randomisation.random_seed import RandomSeed


def main(stdscr: curses.window, args: argparse.Namespace):
    ColorManager.initialise_random_colors()
    args = complete_namespace(stdscr=stdscr, args=args)
    caparams = args_to_params(stdscr = stdscr, args = args)
    player = Player(caparams = caparams)
    player.play()

def initialiseo():
  args = arg_parser()
  RandomSeed.init(seed = args.seed)
  curses.wrapper(main, args)

    
if __name__ == "__main__":
    initialiseo()