from config import Config
from cellular_automaton.rule import Rule


class RuleParse:

  @classmethod
  def validate_rule(rule: str) -> Rule:
      return RuleParse.from_string(rule)
      
  @classmethod  
  def from_string(string: str) -> Rule:
      string = string.upper()
      parts = string.split('/')
      if len(parts) not in (2, 3):
          raise ValueError("expected B.../S...[/aging]")

      b_part, s_part = parts[0], parts[1]
      aging_part = parts[2] if len(parts) == 3 else "1"

      if not b_part.startswith("B") or not s_part.startswith("S"):
          raise ValueError("expected B.../S...[/aging]")

      def parse_digits(part: str) -> set[int]:
          digits = part[1:]
          if not digits: return set()
          if not digits.isdigit(): 
              raise ValueError("invalid digits")
          return {int(c) for c in digits}

      if not aging_part.isdigit() or int(aging_part) < 1 or int(aging_part) > Config.MAX_AGING:
          raise ValueError("invalid aging")

      return Rule(
          born=parse_digits(b_part),
          survive=parse_digits(s_part),
          aging=int(aging_part),
      )