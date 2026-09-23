class UtilsParse():

  @staticmethod
  def parse_float(arg: str, low: float = 0.0, high: float = 1.0) -> float:
      try:
          f = float(arg)
      except ValueError:
          raise ValueError(f"expected a number, got {arg!r}")
      if not low <= f <= high:
          raise ValueError(f"must be 0.0..1.0, got {f}")
      return f

  @staticmethod
  def parse_int(arg: str, low: float | None = None, high: float | None = None) -> int:
    try:
      i = int(arg)
    except ValueError:
      raise ValueError(f"expected a integer, got {arg!r}")
    if low is not None and i < low:
      raise ValueError(f"must be greater than or equal to {low}, got {i}")
    if high is not None and i > high:
      raise ValueError(f"must be less than or equal to {high}, got {i}")
    return i