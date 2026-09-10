from cellular_automaton.rule import Rule
import numpy as np


class Figure:

    def __init__(self, width: int = 20, height: int = 20):
        self.width = width
        self.height = height
        self.generation: np.ndarray = self.buld_frame()

    def buld_frame(self):
        return np.zeros((self.height, self.width), dtype=int)

    def blank_field(self):
        self.generation = self.buld_frame()

    def fill_random(self, fraction: float = 0.5):
        field_size = self.generation.size
        num_ones = int(field_size * fraction)
        idx = np.random.choice(field_size, num_ones, replace=False)
        np.put(self.generation, idx, 1)

    def contain_rect(self, x: int, y: int, width: int = 1, height: int = 1):
        y_start, x_start = y, x
        self.generation[y_start:y_start+height, x_start:x_start+width] = 1

    def contain_rect_in_center(self, width: int, height: int):
        field_heigth = self.generation.shape[0]
        field_width = self.generation.shape[1]
        y_start = (field_heigth - height) // 2
        x_start = (field_width - width) // 2
        self.generation[y_start:y_start+height, x_start:x_start+width] = 1

    

    def next(self, rule: Rule):
        newGeneration = self.buld_frame()
        for i, j in np.ndindex(self.generation.shape):
            value = self.generation[i, j]
            neighbors = self.get_neighbors(i, j)
            match value:
                case 0:
                    if neighbors in rule.born:
                        newGeneration[i, j] = 1
                case 1:
                    if neighbors in rule.survive:
                        newGeneration[i, j] = 1
                    
                    elif rule.aging > 1:
                        newGeneration[i, j] = 2
                case _:
                    if value < rule.aging:
                        newGeneration[i, j] = value + 1
        self.generation = newGeneration

    def get_neighbors(self, i: int, j: int) -> int:
        arr = self.generation
        h, w = arr.shape
        rows = [(i - 1) % h, i, (i + 1) % h]
        cols = [(j - 1) % w, j, (j + 1) % w]
        area = arr[rows, :][:, cols].flatten()
        neighbors = np.delete(area, 4)
        return np.count_nonzero(neighbors == 1)
