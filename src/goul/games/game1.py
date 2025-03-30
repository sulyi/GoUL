import random

from .game_base import GameBase

class Game1(GameBase):
    def __next__(self):
        # Drop off the first y element, append a new one.
        self._state.ydata = self._state.ydata[1:] + [random.randint(0, 10)]
        return self._state

    @classmethod
    def name(cls):
        return "Game 1"