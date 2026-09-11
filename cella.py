import curses

from arg_parser import arg_parser
from cellular_automaton.figure import Figure
from cellular_automaton.rule import Rule
from debug import printl
from player import Player


def main(stdscr):
    args = arg_parser(stdscr)

    rule = Rule.from_string("B2/S0345/10")
    figure = Figure(width=args.width, height=args.height)
    player = Player(stdscr = stdscr, figure=figure, rule=rule)
    player.play()

    
if __name__ == "__main__":
    curses.wrapper(main)