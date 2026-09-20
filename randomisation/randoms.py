from socket import SO_PASSCRED
from numpy.ma import isMaskedArray
from parsing.rule_parse import RuleParse
from config import Config
import numpy as np

from cellular_automaton.rule import Rule
from randomisation.random_seed import RandomSeed

def random_symbols(exclude: str | None = None) -> str:
    symbols = np.array([

        " █▓▒░▫▫·.",
        " ▫▫·.",
        " @%#*+=-:.",
        " @#8&%$o*+=-:.",

        " ●•∙·",
        " @Oo.",
        " #*+-.",
        " ◉●•·˙",
        " @#*?!:;,",
        " █▇▆▅▄▃▂▁",
        " █▉▊▋▌▍▎▏",
        " $@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'.",
        " 123456789",
        " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        " •·",
        " @#*o.",
        " &$Xx+=;:,.",
        " ▓▓▒▒░░",
        " -/|\\",
        " ╳╱╲",
        " I|!:.",
        " @$Xx+=;:.",
        " ○◎◉●•∙·",
        " @%#*;:·˙",
        " @#*:·.",
        " @0Oo·.",
        " ●◉◎○•∙·",
        " ·˙·˙· ",
        
        ])

    if exclude is not None:
        symbols = symbols[symbols != exclude]
    
    return RandomSeed.rng.choice(symbols).item()


def random_rule(exclude: Rule | None = None, aging_only: bool | None = None) -> Rule:
    b = int(RandomSeed.rng.integers(0, 9))
    born = set(RandomSeed.rng.choice(9, b, replace=False)) if b > 0 else set()
    s = int(RandomSeed.rng.integers(0, 9))
    survive = set(RandomSeed.rng.choice(9, s, replace=False)) if s > 0 else set()
    match aging_only:
        case None: aging = int(RandomSeed.rng.integers(1, Config.MAX_RANDOM_AGING + 1))
        case True: aging = int(RandomSeed.rng.integers(2, Config.MAX_RANDOM_AGING + 1))
        case False: aging = 1

    candidate = Rule(born=born, survive=survive, aging=aging)
    return candidate if candidate != exclude else random_rule(exclude=exclude, aging_only=aging_only)

def random_prepared_rule(exclude: str | None = None, aging_posible: bool | None = None) -> Rule:
    rules = np.array([
        "B3/S23", "B3/S12345", "B3/S1234", "B37/S12345", "B37/S1234",
        "B1/S012345678", "B35678/S5678", "B345/S4567", "B2/S0", "B234/S",
        "B234678/S8", "B2345678/S0238", "B234567/S124567", "B235678/S1234567",
        "B3/S45678", "B378/S235678", "B45678/S5678", "B4678/S35678", "B2/S124",
        "B2/S123", "B3/S012358", "B25/S23457", "B278/S0124567", "B26/S012357",
        "B2378/S1234", "B23/S234", "B24567/S", "B2/S0345"
    ])

    rules_a = np.array([
        "B2/S0345/10", "B2/S345/4", "B25/S3467/6", "B2/S3456/6",
        "B26/S0345/6", "B26/S345/5", "B34/S1234/48", "B2/S2/25",
        "B37/S345/3", "B35/S3457/5", "B2356/S1456/16", "B234/S2/5",
        "B23/S145678/8", "B458/S012345/3", "B35/S34578/5", "B34678/S2456/4",
        "B3468/S235678/9", "B1234/S2345/8", "B13/S2/21",
    ])

    if aging_posible is None: 
        selection = np.concatenate([rules, rules_a])
    else: 
        selection = rules_a if aging_posible else rules

    if exclude is not None:
        selection = selection[selection != exclude]
    
    return RuleParse.from_string(RandomSeed.rng.choice(selection).item())