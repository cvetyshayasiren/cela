import argparse
import curses

from parsing.arg_parser import arg_parser, args_to_params
from main.player import Player
from main.colors import ColorManager
from randomisation.random_seed import RandomSeed


def main():
    args = arg_parser()
    RandomSeed.init(seed = args.seed)
    output = curses.wrapper(run, args)
    if(output): print(output)
    

def run(stdscr: curses.window, args: argparse.Namespace):
    curses.curs_set(0)
    ColorManager.initialise_random_colors()
    caparams = args_to_params(stdscr = stdscr, args = args)
    player = Player(caparams = caparams)
    if args.pause: player.pause()
    player.play()
    return player.output

if __name__ == "__main__":
    main()