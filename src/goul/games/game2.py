from goul.games.game_base import GameBase
from goul.games.game_state import GameState


class Game2(GameBase):
    _n_data = 50
    _xdata = list(range(_n_data))
    
    def __init__(self, state):
        super().__init__(state)
        self._count = 0

    def __next__(self):
        self.state.ydata = [self._count for _ in range(self._n_data)]
        self._count += 1
        return self.state

    @classmethod
    def name(cls):
        return "Game 2"

    def get_init_state(self):
        ydata = [0 for _ in range(self._n_data)]
        return GameState(self._xdata, ydata)
