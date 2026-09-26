from __future__ import annotations
from parsing.alignment.window_calc import Size, Offset
from enum import Enum, auto

class Arrangment(Enum):
  TOP_START = auto()
  TOP_CENTER = auto()
  TOP_END = auto()
  CENTER_START = auto()
  CENTER = auto()
  CENTER_END = auto()
  BOTTOM_START = auto()
  BOTTOM_CENTER = auto()
  BOTTOM_END = auto()

  def align(self, outer_box: Size, inner_box: Size) -> Offset:
    x, y = 0, 0
    horizontal_centering = lambda: (outer_box.width - inner_box.width) // 2
    vertical_centering = lambda: (outer_box.height - inner_box.height) // 2
    horizontal_ending = lambda: outer_box.width - inner_box.width
    vertical_ending = lambda: outer_box.height - inner_box.height
  
    match self:
      case Arrangment.TOP_CENTER: x=horizontal_centering()
      case Arrangment.TOP_END: x=horizontal_ending()

      case Arrangment.CENTER_START: y=vertical_centering()
      case Arrangment.CENTER: x=horizontal_centering(); y=vertical_centering()
      case Arrangment.CENTER_END: x=horizontal_ending(); y=vertical_centering()

      case Arrangment.BOTTOM_START: y=vertical_ending()
      case Arrangment.BOTTOM_CENTER: x=horizontal_centering(); y=vertical_ending()
      case Arrangment.BOTTOM_END: x=horizontal_ending(); y=vertical_ending()
      
    return Offset(x,y)
    
  @staticmethod
  def from_id(id: int) -> Arrangment:
    match id:
      case 1: return Arrangment.TOP_START
      case 2: return Arrangment.TOP_CENTER
      case 3: return Arrangment.TOP_END
      case 4: return Arrangment.CENTER_START
      case 5: return Arrangment.CENTER
      case 6: return Arrangment.CENTER_END
      case 7: return Arrangment.BOTTOM_START
      case 8: return Arrangment.BOTTOM_CENTER
      case 9: return Arrangment.BOTTOM_END
    return Arrangment.CENTER