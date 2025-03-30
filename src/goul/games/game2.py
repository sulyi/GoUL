from goul.games.game_base import GameBase
from goul.games.game_state import GameState


class Game2(GameBase):
    def __init__(self, state):
        super().__init__(state)
        self.count = 0

    def __next__(self):
        n_data = 50
        xdata = list(range(n_data))
        ydata = [self.count for i in range(n_data)]
        self.count += 1
        return GameState(xdata, ydata)

    @classmethod
    def name(cls):
        return "Game 2"