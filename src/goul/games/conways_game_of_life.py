import random

from collections import defaultdict
from copy import deepcopy

from .game_base import GameBase
from .game_state import GameState


class DeterministicGame(GameBase):
    _name = "Conway's Game of Life"
    _meta = deepcopy(GameBase._meta)
    _meta["imshow"].update({"origin": "lower"})

    _n_data = 50

    def __next__(self):
        neighbors = (
            (-1, -1),  # Above left
            (-1, 0),  # Above
            (-1, 1),  # Above right
            (0, -1),  # Left
            (0, 1),  # Right
            (1, -1),  # Below left
            (1, 0),  # Below
            (1, 1),  # Below right
        )

        neighbor_count = defaultdict(int)
        for x, y in self.state.cells:
            for offset_x, offset_y in neighbors:
                neighbor_count[(x + offset_x, y + offset_y)] += 1

        stay_alive = {
            cell for cell, count in neighbor_count.items() if 1 < count < 4
        } & self.state.cells
        come_alive = {
            cell for cell, count in neighbor_count.items() if count == 3
        } - self.state.cells

        new_cells = stay_alive | come_alive

        if self.state.cells == new_cells:
            raise StopIteration("No change")

        self.state.cells = new_cells

        return self.state

    def get_init_state(self):
        xdata = [random.randint(0, 10) for _ in range(self._n_data)]
        ydata = [random.randint(0, 10) for _ in range(self._n_data)]

        return GameState({(x, y) for x, y in zip(xdata, ydata)})
