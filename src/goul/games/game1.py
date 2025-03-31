import random

from .game_base import GameBase
from .game_state import GameState


class Game1(GameBase):
    _n_data = 50
    _xdata = list(range(_n_data))

    def __next__(self):
        # Drop off the first y element, append a new one.
        self.state.ydata.pop(0)
        self.state.ydata.append(random.randint(0, 10))
        return self.state

    @classmethod
    def name(cls):
        return "Game 1"

    def get_init_state(self):
        ydata = [random.randint(0, 10) for _ in range(self._n_data)]
        return GameState(self._xdata, ydata)
