import math
import random

from copy import deepcopy

from .game_base import GameBase
from .game_state import GameState


def exponential_distribution(rate):
    return -math.log(random.random()) / rate

class StochasticGameOfLife(GameBase):
    _name = "Stochastic Game of Life"
    _meta = deepcopy(GameBase._meta)
    _meta["imshow"].update({"origin": "lower"})

    _INITIAL_POP_SIZE = 50

    def __init__(self, state, rates=(0.01, 0.01)):
        super().__init__(state)

        self.birth_rate, self.death_rate = rates

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

        total = len(self.state.cells)

        if not self.state.cells:
            raise StopIteration("All cells are dead")

        new_cells = set()
        for _ in range(int(exponential_distribution(self.birth_rate * total))):
            # candidate
            x, y = random.choice(tuple(self.state.cells))

            empty_neighbors = []
            for offset_x, offset_y in neighbors:
                current_neighbor = (x + offset_x, y + offset_y)
                if current_neighbor not in self.state.cells:
                    empty_neighbors.append(current_neighbor)

            if not empty_neighbors:
                # no room for new cell
                continue

            # chose a random neighbor to spawn a new cell
            new_cells.add(random.choice(empty_neighbors))

        for _ in range(int(exponential_distribution(self.death_rate * total))):
            if not self.state.cells:
                break
            self.state.cells.remove(random.choice(tuple(self.state.cells)))

        self.state.cells.update(new_cells)

        return self.state

    def get_init_state(
            self,
            height=GameBase._DEFAULT_INITIAL_HEIGHT,
            width=GameBase._DEFAULT_INITIAL_WIDTH
    ):
        super().get_init_state()
        return GameState.ramdom_state(height, width, self._INITIAL_POP_SIZE)
