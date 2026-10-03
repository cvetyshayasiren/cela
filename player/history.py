from functools import cache
from numpy.typing import NDArray
from collections import deque
import numpy as np

class PlayerHistory:

  def __init__(self, size: int):
    self.history: deque[np.ndarray] = deque(maxlen=size)

  def save(self, generation: np.ndarray):
    self.history.append(generation)

  def take(self) -> np.ndarray:
    return self.history.pop()