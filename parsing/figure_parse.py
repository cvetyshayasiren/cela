from __future__ import annotations
import statistics
from cellular_automaton.figure import Figure
from ty_extensions import Unknown
from numpy import e

import ast
import operator

class FigureParse:
  @staticmethod
  def contain_cells(figure: Figure, aging: int, cells: list[str]):
    cells_list = FigureParse.cell_parse(cells=cells, w=figure.width, h=figure.height, aging=aging)
    for cell in cells_list:
      figure.contain_cell(x=cell.x, y=cell.y, age=cell.a)
  
  @staticmethod
  def cell_parse(cells: list[str], w: int, h: int, aging: int) -> list[Cell]:
    return [ Cell.cell_parse(c, w, h, aging) for c in cells ]
    

class Cell():
  def __init__(self, x: int, y: int, a: int):
    self.x = x
    self.y = y
    self.a = a

  @staticmethod
  def cell_parse(cell: str, w: int, h: int, max_age: int) -> Cell:
    parts = cell.split(":")
    if len(parts) not in (2, 3):
        raise ValueError(f"expected 'x:y[:a]', got {cell!r}")
    x, y = parts[0], parts[1]
    a = parts[2] if len(parts) == 3 else 1

    env: dict[str, int | float] = {"w": w, "h": h, "a": max_age}
    x = int(CellCalculations.eval_expr(parts[0], env))
    y = int(CellCalculations.eval_expr(parts[1], env))
    a = int(CellCalculations.eval_expr(parts[2], env)) if len(parts) == 3 else 1
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
  def _eval(cls: Unknown, node: ast.AST, env: dict[str, float]) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name):
        if node.id not in env:
            raise ValueError(f"unknown variable: {node.id!r}")
        return env[node.id]
    if isinstance(node, ast.BinOp) and type(node.op) in cls._OPS:
        return cls._OPS[type(node.op)](cls._eval(node.left, env), cls._eval(node.right, env))
    if isinstance(node, ast.UnaryOp) and type(node.op) in cls._OPS:
        return cls._OPS[type(node.op)](cls._eval(node.operand, env))
    raise ValueError("invalid expression")

  @classmethod
  def eval_expr(cls: Unknown, expr: str, env: dict[str, float]) -> float:
    tree = ast.parse(expr.strip(), mode="eval").body
    return cls._eval(node=tree, env=env)