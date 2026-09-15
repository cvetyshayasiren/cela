import curses

from main.arg_parser import arg_parser, args_to_params
from main.player import Player


def main(stdscr: curses.window):
    args = arg_parser(stdscr)
    caparams = args_to_params(stdscr = stdscr, args = args)
    player = Player(caparams = caparams)
    player.play()

    
if __name__ == "__main__":
    curses.wrapper(main)