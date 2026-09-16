from main.colors import ColorManager
from randomisation.random_seed import RandomSeed


def initialise(seed):
    RandomSeed.init(seed=seed)
    ColorManager.initialise_random_colors()