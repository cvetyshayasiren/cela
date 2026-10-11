from __future__ import annotations
from abc import ABC, abstractmethod

from numpy.typing import NDArray
from collections import deque
import numpy as np


class PlayerHistory(ABC):

  @abstractmethod
  def save(self, generation: np.ndarray):
    ...

  @abstractmethod
  def undo(self) -> np.ndarray:
    ...

  @abstractmethod
  def is_stuck(self, generation: np.ndarray) -> int:
    ...

  @staticmethod
  def from_size(size: int, generation: np.ndarray) -> PlayerHistory:
    if(size == 1): return PlayerHistoryValue(generation)
    return PlayerHistoryDeque(size=size, generation=generation)

class PlayerHistoryValue(PlayerHistory):
  def __init__(self, generation: np.ndarray):
    self.old_generation = generation

  def save(self, generation: np.ndarray):
    self.old_generation = generation

  def undo(self) -> np.ndarray: return self.old_generation

  def is_stuck(self, generation: np.ndarray) -> int:
    if self.old_generation == generation: return 1
    return 0

class PlayerHistoryDeque(PlayerHistory):
  def __init__(self, size: int, generation: np.ndarray):
    self.history: deque[np.ndarray] = deque(maxlen=size)
    self.save(generation)

  def save(self, generation: np.ndarray) -> int:
    self.history.append(generation)

  def undo(self) -> np.ndarray:
    if len(self.history) > 1: return self.history.pop()
    return self.history[0]

  def is_stuck(self, generation: np.ndarray) -> int:
    for i, state in enumerate(reversed(self.history)):
        if np.array_equal(state, generation):
            return i + 1
    return 0