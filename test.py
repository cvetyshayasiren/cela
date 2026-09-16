import numpy as np

from main.ca_params import StuckBehaviour
from randomisation.random_seed import RandomSeed

def main():
    l = [i.lower() for i in StuckBehaviour.__members__]
    print(l)

if __name__ == "__main__":
    main()