import argparse
import curses

from main.arg_parser import arg_parser, args_to_params, complete_namespace
from main.player import Player
from main.colors import ColorManager
from randomisation.random_seed import RandomSeed


def main():
    args = arg_parser()
    RandomSeed.init(seed = args.seed)
    curses.wrapper(run, args)

def run(stdscr: curses.window, args: argparse.Namespace):
    curses.curs_set(0)
    ColorManager.initialise_random_colors()
    args = complete_namespace(stdscr=stdscr, args=args)
    caparams = args_to_params(stdscr = stdscr, args = args)
    player = Player(caparams = caparams)
    player.play()

if __name__ == "__main__":
    main()