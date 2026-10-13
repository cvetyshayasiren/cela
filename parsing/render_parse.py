from render.colors import HslColor, RgbColor
from parsing.utils_parse import UtilsParse
from alignment.arrangement import Arrangment
import alignment
from alignment.window_calc import Offset


class RenderParse:

  @staticmethod
  def validate_offset(arg: str) -> Offset:
    return RenderParse.parse_offset(arg = arg)

  @staticmethod
  def validate_align(arg: str) -> Arrangment:
    return RenderParse.parse_arrangment(arg)

  @staticmethod
  def validate_hex(arg: str) -> HslColor:
    return RenderParse.parse_hex(arg)

  @staticmethod
  def parse_offset(arg: str) -> Offset:
    parts = arg.split(":")
    if len(parts) != 2:
        raise ValueError(f"expected 'x:y', got {arg!r}")
    try:
        x, y = int(parts[0]), int(parts[1])
    except ValueError:
        raise ValueError(f"invalid numbers in {arg!r}")
    return Offset(x,y)

  @staticmethod
  def parse_arrangment(arg: str) -> Arrangment:
    id = UtilsParse.parse_int(arg=arg, low=1, high=9)
    return Arrangment.from_id(id)

  @staticmethod
  def parse_hex(arg: str) -> HslColor:
    v = arg.lstrip("#")
    if len(v) != 6 or not all(c in "0123456789abcdefABCDEF" for c in v):
        raise ValueError(f"expected hex color like #RRGGBB, got {arg!r}")
    r = int(v[0:2], 16)
    g = int(v[2:4], 16)
    b = int(v[4:6], 16)
    return RgbColor(red = r*1000//255, green = g*1000//255, blue = b*1000//255).to_hsl()

    