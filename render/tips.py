from __future__ import annotations

from enum import Enum, auto
from config import Config
import curses
from main.ca_params import Caparams

class Tips:

  def __init__(self, caparams: Caparams):
    self.caparams: Caparams = caparams
    self.tips_mode: TipsMode = TipsMode.MINI
    self.tips_win: curses.window = self._make_tips_window()
    self.tips_full_string: str = self.make_tips_full_string()
    self.tips_mini_string: str = self.make_tips_mini_string()
    self.offset: int = 0

  def draw_tips(self):
    self.tips_win.clear()
    if(self.tips_mode == TipsMode.MINI): self.draw_mini()
    if(self.tips_mode == TipsMode.FULL): self.draw_full()
    self.tips_win.noutrefresh()
    

  def draw_mini(self):
    self.tips_win.addstr(self.make_tips_mini_string())

  def draw_full(self):
    self.tips_win.addstr(self.make_tips_full_string())
    self.tips_win.box()

  def _make_tips_window(self) -> curses.window:
    term_size = self.caparams.getTermSize()
    win_height = int(term_size.height * Config.TIPS_HEIGHT_FRACTION)
    return curses.newwin(
        win_height, term_size.width, term_size.height - win_height, 0
    )

  def make_tips_full_string(self) -> str:
    header = f"rule {self.caparams.rule.string}"
    output = self.embed_a_string(header)
    tips_list: list[str] = [
      f"q - exit",
      "p - pause/resume",
      "r - randomise field",
      "c - randomise color",
      "s - randomise symbols",
      "(1-9) - add square in center",
      "b - blank field",
    ]
    for t in tips_list:
      output += (self.divider() + self.embed_a_string(t))
    
    return output

  def make_tips_mini_string(self):
    paused = self.caparams.paused
    size_string = f"{self.caparams.figure.width}x{self.caparams.figure.height}"
    pause_state_string = "PAUSED.." if paused else "playing"
    candidate = f"{pause_state_string}|{size_string}|i - info/tips"
    return candidate[:self.width_without_box()]

  def toogle_tips(self): 
    self.tips_mode = TipsMode.next(self.tips_mode)
    self.draw_tips()
  
  def embed_a_string(self, string: str) -> str:
    width = self.width_without_box()
    chunks = [string[i:i+width] for i in range(0, len(string), width)]
    return "\n".join(chunks)

  def divider(self) -> str:
    width = self.width_without_box()
    return f"""\n{"-" * width}\n"""

  def width_without_box(self) -> int: return self.caparams.getTermWidth() - 2


class TipsMode(Enum):
  HIDDEN = auto()
  MINI = auto()
  FULL = auto()

  @classmethod
  def next(cls, mode: TipsMode) -> TipsMode:
      members = list(cls)
      return members[(members.index(mode) + 1) % len(members)]