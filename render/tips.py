from main.ca_params import Caparams

class Tips:

  def __init__(self, caparams: Caparams):
    self.caparams: Caparams = caparams
    self.tips = self.make_tips()

  def make_tips(self) -> str:
    output = ""
    header = f"rule {self.caparams.rule.string}"
    tips_list: list[str] = [
      f"q - exit",
      "p - pause/resume",
      "r - randomise field",
      "c - randomise color",
      "s - randomise symbols",
      "(1-9) - add square in center",
      "b - blank field",
    ]
    
    return output

  def embed_a_string(self, string: str) -> str:
    term_width = self.caparams.getTermSize().width
    chunks = [string[i:i+term_width] for i in range(0, len(string), term_width)]
    return ""

  def divider(self):
    width = self.caparams.getTermWidth()
    return f"""\n{"-" * width}\n"""

  