
class Config:
    MIN_DELAY: int = 1
    MAX_DELAY: int = 60_000
    MAX_AGING: int = 100
    MAX_RANDOM_AGING: int = 10

    MIN_DIMENSION: int = 1
    MAX_DIMENSION: int = 400

    TIPS_HEIGHT_FRACTION: float = 0.8

    DEFAULT_HISTORY_SIZE: int = 10