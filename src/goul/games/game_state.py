from dataclasses import dataclass
from typing import List


@dataclass
class GameState:
    xdata: List[int]
    ydata: List[int]

    @property
    def data(self):
        # Convert sparse data to binary matrix
        min_x = min(self.xdata)
        min_y = min(self.ydata)

        width = max(self.xdata) - min_x + 1
        height = max(self.ydata) - min_y + 3

        data = [[0 for _ in range(width)] for _ in range(height)]

        for x, y in zip(self.xdata, self.ydata):
            data[y - min_y + 1][x - min_x] = 1

        return data
