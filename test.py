from numpy.ma import in1d
import curses
import numpy as np

from main.ca_params import StuckBehaviour
from randomisation.random_seed import RandomSeed

def main_test():
    string = "lalkeklol keklollal kekelolo lalalol"
    s = embed_a_string(string, 4)
    print(s)

def embed_a_string(string: str, width: int) -> list[str]:
    chunks = [string[i:i+width] for i in range(0, len(string), width)]
    return chunks
    

if __name__ == "__main__":
    main_test()