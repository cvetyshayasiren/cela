from parsing.utils_parse import UtilsParse
from alignment.arrangement import Arrangment
import alignment
from alignment.window_calc import Offset


class RenderParse:

  @staticmethod
  def validate_offset(arg: str) -> Offset:
    return RenderParse.parse_offset(arg = arg)

  def validate_align(arg: str) -> Arrangment:
    return RenderParse.parse_arrangment(arg)

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