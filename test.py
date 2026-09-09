import numpy as np

from cellular_automaton.figure import Figure

def main():
    fig = Figure(width=10, height=5)
    fig.fill_random()
    print(fig.generation)
    n = fig.get_neighbors(4, 0)
    print(n)

if __name__ == "__main__":
    main()

