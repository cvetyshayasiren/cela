import curses
import logging


def printd(message: str):
    debug_win = curses.newwin(5, 50, 0, 0)
    debug_win.addstr(0, 0, str(message))
    debug_win.refresh()

def printl(message: str):
    logging.basicConfig(filename="debug.log", level=logging.DEBUG)
    logging.debug(f"log: {message}")