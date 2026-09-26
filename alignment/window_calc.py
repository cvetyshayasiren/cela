from __future__ import annotations
from typing import ClassVar

import curses
from dataclasses import dataclass, field

@dataclass
class Size:
  width: int
  height: int

  def center(self) -> Offset:
    return Offset(self.width//2, self.height//2)
    
  @staticmethod
  def from_curses_window(window: curses.window) -> Size:
    h, w = window.getmaxyx()
    return Size(width=w, height=h)
    
@dataclass
class Offset:
  x: int = field(default_factory=lambda: 0)
  y: int = field(default_factory=lambda: 0)