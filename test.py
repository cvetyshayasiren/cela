import numpy as np
import time
import curses

from cellular_automaton.figure import Figure
from cellular_automaton.rule import Rule
from player import Player

def main(stdscr):
    rule = Rule.from_string("B2/S0345/10")
    h, w = stdscr.getmaxyx()
    fig = Figure(width=w, height=h)
    fig.fill_random(0.2)
    player = Player(stdscr = stdscr, figure=fig, rule=rule)
    player.play()



if __name__ == "__main__":
    curses.wrapper(main)

