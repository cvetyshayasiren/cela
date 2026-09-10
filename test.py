import numpy as np
import time
import curses

from cellular_automaton.figure import Figure
from cellular_automaton.rule import Rule

def main(stdscr):
    rule = Rule(born = {2}, survive={3,4,5}, aging=4)
    fig = Figure(width=200, height=40)
    fig.contain_rect(3, 3)
    frame = 0
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    while(True):
        stdscr.clear()
        frame += 1
        stdscr.addstr(drawFigure(fig))
        stdscr.refresh()
        fig.next(rule=rule)
        time.sleep(0.02)
    
        


def drawFigure(figure: Figure) -> str:
    symbols = np.array([" ", "o", "O", "A", "B", "C"])
    output_string = ""
    for i, j in np.ndindex(figure.generation.shape):
        if i > 0 and j == 0:
            output_string += "\n"
        value = figure.generation[i, j]
        output_string += symbols[value]
    return output_string



if __name__ == "__main__":
    curses.wrapper(main)

