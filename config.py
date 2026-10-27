
class Config:
    MIN_DELAY: int = 1
    MAX_DELAY: int = 60_000
    MAX_AGING: int = 100
    MAX_RANDOM_AGING: int = 10

    MIN_DIMENSION: int = 1
    MAX_DIMENSION: int = 400

    TIPS_HEIGHT_FRACTION: float = 0.8

    DEFAULT_HISTORY_SIZE: int = 10

    BASE_SYMBOLS_LIST: list[str] = [" ", "■"]

    DEFAULT_PAUSE_STRING: str = "PAUSED.."

    MIN_SATURATION: float = 0.4
    MAX_SATURATION: float = 1.0
    MIN_LIGHTNESS: float = 0.4
    MAX_LIGHTNESS: float = 1.0
    BG_SATURATION: float = 0.2
    BG_LIGHTNESS: float = 0.2

    MIN_GRADIENT_STEP: float = 0.5 # hue degree
    MAX_GRADIENT_STEP: float = 60.0  # hue degree