def coerce_in_int(low: int, high: int, value: int) -> int:
  return max(low, min(high, value))

def coerce_in_float(low: float, high: float, value: float) -> float:
  return max(low, min(high, value))

def coerce_at_least_int(low: int, value: int) -> int:
  return max(low, value)

def coerce_at_least_float(low: float, value: float) -> float:
  return max(low, value)

def coerce_at_most_int(high: int, value: int) -> int:
  return min(high, value)

def coerce_at_most_float(high: float, value: float) -> float:
  return min(high, value)

def lerp(start: float, end: float, fraction: float) -> float:
  return start + (end - start) * fraction

def lerp_clamped(start: float, end: float, fraction: float) -> float:
  t = coerce_in_float(0.0, 1.0, fraction)
  return start + (end - start) * fraction
  