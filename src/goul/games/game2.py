from copy import deepcopy

from goul.games.game_base import GameBase
from goul.games.game_state import GameState


class Game2(GameBase):
    _name = "Game 2"
    _meta = deepcopy(GameBase._meta)
    _meta["imshow"].update({"origin": "lower"})

    _n_data = 50

    def __init__(self, state):
        super().__init__(state)
        self._count = 0

    def __next__(self):
        self.state.cells = {(x, self._count) for x, _ in self.state.cells}
        self._count += 1
        return self.state

    def get_init_state(self):
        return GameState({(x, 0) for x in range(self._n_data)})
