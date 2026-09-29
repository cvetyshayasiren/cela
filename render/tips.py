from enum import Enum, auto
from config import Config
import curses
from main.ca_params import Caparams

class Tips:

  def __init__(self, caparams: Caparams):
    self.caparams: Caparams = caparams
    self.tips_win = self._make_tips_window()
    self.tips = self.make_tips()

  def _make_tips_window(self) -> curses.window:
    term_size = self.caparams.getTermSize()
    win_height = int(term_size.height * Config.TIPS_HEIGHT_FRACTION)
    return curses.newwin(
        win_height, term_size.width, term_size.height - win_height, 0
    )

  def make_tips(self) -> str:
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

  def embed_a_string(self, string: str) -> str:
    term_width = self.caparams.getTermSize().width
    chunks = [string[i:i+term_width] for i in range(0, len(string), term_width)]
    return "\n".join(chunks)

  def divider(self) -> str:
    width = self.caparams.getTermWidth()
    return f"""\n{"-" * width}\n"""


class TipsMode(Enum):
  HIDDEN = auto()
  MINI = auto()
  FULL = auto()

  @classmethod
  def next(cls, mode: TipsMode) -> TipsMode:
      members = list(cls)
      return members[(members.index(mode) + 1) % len(members)]