from dataclasses import dataclass

@dataclass
class GameState:
    cells: set[tuple[int, int]]

    @property
    def data(self):
        # Convert sparse data to binary matrix
        min_x = min(x for x, _ in self.cells)
        min_y = min(y for _, y in self.cells)

        width = max(x for x, _ in self.cells) - min_x + 1
        height = max(y for _, y in self.cells) - min_y + 3

        data = [[0 for _ in range(width)] for _ in range(height)]

        for x, y in self.cells:
            data[y - min_y + 1][x - min_x] = 1

        return data
