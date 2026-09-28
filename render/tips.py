from main.ca_params import Caparams

class Tips:

  def __init__(self, caparams: Caparams):
    self.caparams = caparams
    self.tips = self.make_tips()

  def make_tips(self) -> str:
    tips_list: list[str] = [
      f"q - exit",
      "p - pause/resume",
      "r - randomise field",
      "c - randomise color",
      "s - randomise symbols",
      "(1-9) - add square in center",
      "b - blank field",
      f"rule {self.caparams.rule.string}"
    ]
    return ""

  