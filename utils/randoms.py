import random

import numpy as np

from cellular_automaton.rule import Rule

def random_symbols() -> str:
    symbols = np.array([

        " █▓▒░▫▫·.",
        " ▫▫·.",
        " @%#*+=-:.",
        " @#8&%$o*+=-:.",

        " █▓▒░"
        ])

    return np.random.choice(symbols)


def random_rule() -> Rule:
    born = set(random.sample(range(9), random.randint(0, 8)))
    survive = set(random.sample(range(9), random.randint(0, 8)))
    aging = random.randint(0, 8)
    return Rule(born=born, survive=survive, aging=aging)

def random_prepared_rule() -> Rule:
    rules = []
    return Rule()