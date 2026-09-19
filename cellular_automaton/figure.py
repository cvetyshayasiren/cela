from cellular_automaton.rule import Rule
import numpy as np
from randomisation.random_seed import RandomSeed


class Figure:

    def __init__(self, width: int = 20, height: int = 20):
        self.width = width
        self.height = height
        self.generation: np.ndarray = self.buld_frame()

    def buld_frame(self):
        return np.zeros((self.height, self.width), dtype=int)

    def blank_field(self):
        self.generation[:] = 0

    def fill_random(self, fraction: float = 0.5):
        num_ones = int(self.generation.size * fraction)
        flat = self.generation.ravel()
        flat[:] = 0
        idx = RandomSeed.rng.choice(flat.size, num_ones, replace=False)
        flat[idx] = 1

    def fill_full_random(self): self.fill_random(fraction = RandomSeed.rng.random())

    def contain_rect(self, x: int, y: int, width: int = 1, height: int = 1):
        y_start = max(0, y); x_start = max(0, x)
        self.generation[y_start:y_start+height, x_start:x_start+width] = 1

    def contain_rect_in_center(self, width: int, height: int):
        y_start = (self.height - height) // 2
        x_start = (self.width - width) // 2
        self.contain_rect(x=x_start, y=y_start, width=width, height=height)

    def contain_cell(self, x: int, y: int, age: int):
        if(x > self.width or y > self.height): return
    
    def toogle_cell(self, x: int, y: int):
        if(x > self.width or y > self.height): return
        value = self.generation[y, x]
        self.generation[y, x] = 0 if value else 1

    def next(self, rule: Rule) -> bool:
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
        equal = np.array_equal(self.generation, newGeneration)
        self.generation = newGeneration
        return not equal

    def get_neighbors(self, i: int, j: int) -> int:
        arr = self.generation
        h, w = arr.shape
        rows = [(i - 1) % h, i, (i + 1) % h]
        cols = [(j - 1) % w, j, (j + 1) % w]
        area = arr[rows, :][:, cols].flatten()
        neighbors = np.delete(area, 4)
        return np.count_nonzero(neighbors == 1)
