from __future__ import annotations
from parsing.arg_parser import parse_or_raise
import stat
from numpy.distutils.extension import Extension
from dataclasses import dataclass
import dataclasses
import statistics
from cellular_automaton.figure import Figure
from numpy import e

import ast
import operator

class FigureParse:
  @staticmethod
  def validate_contain(contain: str) -> Cell:
    return parse_or_raise("contain", Cell.validate, contain)

  @staticmethod
  def contain_cells(figure: Figure, max_age: int, cells: list[Cell]):
    for cell in cells:
      cell.contain(figure=figure, max_age=max_age)

  @staticmethod
  def validate_rect(rect: str) ->tuple[int, int]:
      return parse_or_raise("rect", FigureParse.rect_parse, rect)
    
  @staticmethod
  def rect_parse(arg: str) -> tuple[int, int]:
    parts = arg.split(":")
    if len(parts) != 2:
        raise ValueError(f"expected 'width:height', got {arg!r}")
    try:
        w, h = int(parts[0]), int(parts[1])
    except ValueError:
        raise ValueError(f"invalid numbers in {arg!r}")
    if w <= 0 or h <= 0:
        raise ValueError(f"width and height must be > 0, got {w}:{h}")
    return w, h

  @staticmethod
  def contain_rect(figure: Figure, rect: tuple[int, int]):
    figure.contain_rect_in_center(width=rect[0], height=rect[1])
    
@dataclass
class Cell():
  x: ast.AST
  y: ast.AST
  a: ast.AST

  def contain(self, figure: Figure, max_age: int):
    env: dict[str, int | float] = {"w": figure.width, "h": figure.height, "a": max_age}
    x = CellCalculations.eval_expr(node = self.x, env=env)
    y = CellCalculations.eval_expr(node = self.y, env=env)
    a = CellCalculations.eval_expr(node = self.a, env=env)
    figure.contain_cell(x=x, y=y, age=a)

  @staticmethod
  def validate(cell: str) -> Cell:
    parts = cell.split(":")
    if len(parts) not in (2, 3):
        raise ValueError(f"expected 'x:y[:a]', got {cell!r}")
    x, y = parts[0], parts[1]
    a = parts[2] if len(parts) == 3 else "1"

    x = CellCalculations.parse_expr(x)
    y = CellCalculations.parse_expr(y)
    a = CellCalculations.parse_expr(a)
    return Cell(x, y, a)

  
class CellCalculations():

  _OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
  }

  @classmethod
  def parse_expr(cls: type["CellCalculations"], expr: str, allowed: set[str] = {"w", "h", "a"}) -> ast.AST:
    try:
        node = ast.parse(expr.strip(), mode="eval").body
    except SyntaxError as e:
        raise ValueError(f"syntax error in {expr!r}: {e}")
    cls._validate(node, allowed)
    return node

  @classmethod
  def eval_expr(cls: type["CellCalculations"], node: ast.AST, env: dict[str, float]) -> int:
    return int(cls._eval(node, env))

  @classmethod
  def _validate(cls: type["CellCalculations"], node: ast.AST, allowed: set[str]) -> None:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return
    if isinstance(node, ast.Name):
        if node.id not in allowed:
            raise ValueError(f"unknown variable: {node.id!r}")
        return
    if isinstance(node, ast.BinOp):
        if type(node.op) not in cls._OPS:
            raise ValueError(f"unsupported operator: {type(node.op).__name__}")
        cls._validate(node.left, allowed)
        cls._validate(node.right, allowed)
        return
    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in cls._OPS:
            raise ValueError(f"unsupported operator: {type(node.op).__name__}")
        cls._validate(node.operand, allowed)
        return
    raise ValueError(f"unsupported node: {type(node).__name__}")

  @classmethod
  def _eval(cls: type["CellCalculations"], node: ast.AST, env: dict[str, float]) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name):
        if node.id not in env:
            raise ValueError(f"unknown variable: {node.id!r}")
        return env[node.id]
    if isinstance(node, ast.BinOp):
        return cls._OPS[type(node.op)](cls._eval(node.left, env), cls._eval(node.right, env))
    if isinstance(node, ast.UnaryOp):
        return cls._OPS[type(node.op)](cls._eval(node.operand, env))
    raise ValueError(f"unsupported node: {type(node).__name__}")

  

    