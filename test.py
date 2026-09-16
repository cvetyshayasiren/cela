import numpy as np

from randomisation.random_seed import RandomSeed

def main():
    print("test")
    print(np.random.SeedSequence().entropy)

if __name__ == "__main__":
    main()