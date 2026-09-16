import numpy as np

class RandomSeed:
    rng: np.random.Generator = None
    seed: int = None

    @classmethod
    def init(cls, seed):
        cls.rng = np.random.default_rng(seed)
        cls.seed = seed