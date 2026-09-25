from numpy.ma import in1d
import curses
import numpy as np

from main.ca_params import StuckBehaviour
from randomisation.random_seed import RandomSeed

def main_test(stdscr):
    stdscr.refresh()
    win = curses.newwin(20, 50, 0, 0)
    win.addstr(2, 2, f"Hello Hello brother\n{'-' * 50}\nwatafak what are you doing?\n{'-' * 50}\nehehe lol kek lal")
    win.box()
    win.refresh()
    stdscr.getch()
    

if __name__ == "__main__":
    curses.wrapper(main_test)