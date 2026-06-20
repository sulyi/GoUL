from dataclasses import dataclass

@dataclass
class GameState:
    cells: set[tuple[int, int]]

    def __bool__(self):
        return bool(self.cells)

    @property
    def data(self):
        if not self.cells:
            return []

        # Convert sparse data to binary matrix
        min_x = min(x for x, _ in self.cells)
        min_y = min(y for _, y in self.cells)

        padding = 1
        width = max(x for x, _ in self.cells) - min_x + 2 * padding
        height = max(y for _, y in self.cells) - min_y + 2 * padding

        data = [[0 for _ in range(width)] for _ in range(height)]

        for x, y in self.cells:
            data[y - min_y + padding][x - min_x + padding] = 1

        return data
