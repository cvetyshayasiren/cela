from __future__ import annotations

import curses
from dataclasses import dataclass

@dataclass
class WindowCalc:
  width: int
  height: int

  @staticmethod
  def from_curses_window(window: curses.window) -> WindowCalc:
    h, w = window.getmaxyx()
    return WindowCalc(width=w, height=h)
    
    