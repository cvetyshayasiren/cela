from __future__ import annotations
from debug import printl
from alignment.window_calc import Size

from enum import Enum, auto
from config import Config
import curses
from caparams.ca_params import Caparams

class Tips:

  def __init__(self, caparams: Caparams):
    self.caparams: Caparams = caparams
    self.tips_mode: TipsMode = TipsMode.MINI
    self.tips_win: curses.window = self._make_tips_window()
    self.tips_win_size: Size = Size.from_curses_window(self.tips_win)
    self.tips_full_lines_list: list[str] = self._make_tips_full_lines_list()
    self.pause_message: str = ""
    self.tips_mini_string: str = self._make_tips_mini_string()
    self.offset: int = 0
    self.max_offset: int = self._calculate_max_offset()

  def set_pause_message(self, message: str): self.pause_message = f"[{message}]"
  def reset_pause_message(self): self.pause_message = ""
  
  def toogle_tips(self) -> TipsMode: 
    self.tips_mode = TipsMode.next(self.tips_mode)
    return self.tips_mode
  
  def can_move_down(self) -> bool: return self.offset < self.max_offset
  def can_move_up(self) -> bool: return self.offset > 0

  def move_down(self):
    if self.can_move_down(): self.offset += 1

  def move_up(self):
    if self.can_move_up(): self.offset -= 1
  
  def draw_tips(self, win: curses.window):
    if self.tips_mode == TipsMode.HIDDEN: return
    self.tips_win.erase()
    if(self.tips_mode == TipsMode.MINI): self._draw_mini(win)
    if(self.tips_mode == TipsMode.FULL): self._draw_full(win)

  def _draw_mini(self, win: curses.window):
    y = self.tips_win_size.height - 2
    self.tips_win.addstr(y, 1, self._make_tips_mini_string())
    self.tips_win.overlay(win)
    
  def _draw_full(self, win: curses.window):
    for index, line in enumerate(self._get_current_full_range()):
      self.tips_win.addstr(index + 1, 1, line)
    self.tips_win.box()
    self.tips_win.overwrite(win)

  def _calculate_max_offset(self) -> int:
    return max(0, self._count_tips_full_lines() - self._height_without_box())

  def _count_tips_full_lines(self) -> int:
    return len(self.tips_full_lines_list)
  
  def _get_current_full_range(self) -> list[str]:
    start: int = self.offset
    end: int = min(start + self._height_without_box(), self._count_tips_full_lines())
    return self.tips_full_lines_list[start:end]

  def _make_tips_window(self) -> curses.window:
    term_size = self.caparams.getTermSize()
    win_height = int(term_size.height * Config.TIPS_HEIGHT_FRACTION)
    return curses.newwin(
        win_height, term_size.width, term_size.height - win_height, 0
    )

  def _make_tips_full_lines_list(self) -> list[str]:
    header: str = self._rule_string()
    full_string: str = self._embed_a_string(header)
    tips_list: list[str] = [
      f"q - exit",
      "p - pause/resume",
      "r - randomise field",
      "c - randomise color",
      "s - randomise symbols",
      "(1-9) - add square in center",
      "b - blank field",
    ]

    ###TODO DELETE
    tips_list += [str(i) for i in range(40)]
    ###/TODO
    
    for t in tips_list:
      full_string += (self._divider() + self._embed_a_string(t))
    
    return full_string.splitlines()

  def _make_tips_mini_string(self):
    paused = self.caparams.paused
    size_string = f"{self.caparams.figure.width}x{self.caparams.figure.height}"
    pause_state_string = "PAUSED.." if paused else ""
    candidate = (
      f"{self.pause_message}{pause_state_string} {size_string} | "
      f"i - info | delay {self.caparams.delay} ms. {self._rule_string()}"
    )
    return candidate[:self._width_without_box()]

  def _rule_string(self) -> str: return f"rule {self.caparams.rule.string}"
    
  def _embed_a_string(self, string: str) -> str:
    width = self._width_without_box()
    chunks = [string[i:i+width] for i in range(0, len(string), width)]
    return "\n".join(chunks)

  def _divider(self) -> str:
    width = self._width_without_box()
    return f"""\n{"-" * width}\n"""

  def _width_without_box(self) -> int: return self.tips_win_size.width - 2
  def _height_without_box(self) -> int: return self.tips_win_size.height - 2


class TipsMode(Enum):
  HIDDEN = auto()
  MINI = auto()
  FULL = auto()

  @classmethod
  def next(cls, mode: TipsMode) -> TipsMode:
      members = list(cls)
      return members[(members.index(mode) + 1) % len(members)]