from __future__ import annotations
from enum import Enum, auto

class StuckBehaviour(Enum):
  PAUSE = auto()
  CONTINUE = auto()
  STOP = auto()

  @classmethod
  def next(cls, mode: StuckBehaviour) -> StuckBehaviour:
      members = list(cls)
      return members[(members.index(mode) + 1) % len(members)]