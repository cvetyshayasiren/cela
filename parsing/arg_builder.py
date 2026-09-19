from randomisation.random_seed import RandomSeed
from main.ca_params import Caparams
from cellular_automaton.figure import Figure
import numpy as np

class ArgBuilder():

  @staticmethod
  def build_args_string(caparams: Caparams) -> str:
    args = (
      f"python cela.py -b -p -W {caparams.figure.width} -H {caparams.figure.height} -d {caparams.delay}"
      f""" -r {caparams.rule.string} -s "{caparams.get_symbols_string()}" -S {caparams.seed}"""
    )
    contains = ArgBuilder.figure_to_contains(figure=caparams.figure)
    if contains: args += f" --contain{contains}"
    return args
    

  @staticmethod
  def figure_to_contains(figure: Figure):
    contains = ""
    for i, j in np.ndindex(figure.generation.shape):
      value = figure.generation[i, j]
      if(value > 0):
        contains += f" {j}:{i}:{value}"
    return contains