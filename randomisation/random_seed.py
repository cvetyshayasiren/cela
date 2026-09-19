import numpy as np

class RandomSeed:
    rng: np.random.Generator
    seed: int

    @classmethod
    def init(cls, seed: int):
        if seed is None:
            seed = np.random.SeedSequence().entropy
        cls.rng = np.random.default_rng(seed)
        cls.seed = seed