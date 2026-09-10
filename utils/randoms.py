import numpy as np

def random_symbols() -> str:
    symbols = np.array([

        " █▓▒░▫▫·.",
        " ▫▫·.",
        " @%#*+=-:.",
        " @#8&%$o*+=-:.",

        " █▓▒░"
        ])

    return np.random.choice(symbols)