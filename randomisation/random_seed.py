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

    @classmethod
    def random_bool(cls) -> bool:
        return cls.rng.integers(0, 2, dtype=bool)