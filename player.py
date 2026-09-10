import time

from cellular_automaton.figure import Figure
from cellular_automaton.rule import Rule
from render import Render


class Player:

    def __init__(self, stdscr,
                 figure: Figure = Figure(), 
                 rule: Rule = Rule(),
                 delay: float = 0.1
                 ):
        self.stdscr = stdscr
        self.figure = figure
        self.rule = rule
        self.delay = delay
        self.render = Render(stdscr, figure, rule.aging)
        self.is_playing: bool = False

    def play(self):
        self.is_playing = True
        self.stdscr.timeout(int(self.delay * 1000))

        while(self.is_playing == True):
            key = self.stdscr.getch()
            if key == ord('s'):
                self.is_playing = False
                break

            self.figure.next(rule=self.rule)
            self.render.draw()

    def stop(self):
        self.is_playing = False