from cellular_automaton.rule import Rule
import numpy as np


class Figure:

    def __init__(
            self, 
            delay: float = 0.1, 
            width: int = 20, 
            height: int = 20, 
            rule: Rule = Rule.from_string("B2/S0345/10")
            ):
        self.delay = delay
        self.width = width
        self.height = height
        self.rule = rule
        self.generation: np.ndarray = self.buld_frame()

    def buld_frame(self):
        return np.zeros((self.height, self.width))

    def fill_random(self, fraction: float = 0.5):
        field_size = self.generation.size
        num_ones = int(field_size * fraction)
        idx = np.random.choice(field_size, num_ones, replace=False)
        np.put(self.generation, idx, 1)

    def contain_rect(self, width: int, height: int):
        field_heigth = self.generation.shape[0]
        field_width = self.generation.shape[1]
        y_start = (field_heigth - height) // 2
        x_start = (field_width - width) // 2
        self.generation[y_start:y_start+height, x_start:x_start+width] = 1

    def next(self, rule: Rule) -> Figure:
        for i, j in np.ndindex(self.generation):
            value = self.generation[i, j]

    def get_neighbors(self, i: int, j: int) -> np.ndarray:
        arr = self.generation
        h, w = arr.shape
        rows = [(i - 1) % h, i, (i + 1) % h]
        cols = [(j - 1) % w, j, (j + 1) % w]
        result = arr[rows, :][:, cols].flatten()
        return np.delete(result, 4)
