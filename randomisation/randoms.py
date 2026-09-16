import numpy as np

from cellular_automaton.rule import Rule
from randomisation.random_seed import RandomSeed

def random_symbols() -> str:
    symbols = np.array([

        " █▓▒░▫▫·.",
        " ▫▫·.",
        " @%#*+=-:.",
        " @#8&%$o*+=-:.",

        " █▓▒░"
        ])

    return RandomSeed.rng.choice(symbols)


def random_rule() -> Rule:
    b = int(RandomSeed.rng.integers(0, 9))
    born = set(RandomSeed.rng.choice(9, b, replace=False)) if b > 0 else set()
    s = int(RandomSeed.rng.integers(0, 9))
    survive = set(RandomSeed.rng.choice(9, s, replace=False)) if s > 0 else set()
    aging = RandomSeed.rng.integers(0, 11)
    return Rule(born=born, survive=survive, aging=aging)

def random_prepared_rule() -> Rule:
    rules = []
    return Rule()