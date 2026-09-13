import curses

from arg_parser import arg_parser, args_to_params
from cellular_automaton.figure import Figure
from cellular_automaton.rule import Rule
from debug import printl
from player import Player


def main(stdscr):
    args = arg_parser(stdscr)
    caparams = args_to_params(stdscr= stdscr, args= args)

    player = Player(stdscr = stdscr, figure=figure, rule=rule)
    player.play()

    
if __name__ == "__main__":
    curses.wrapper(main)