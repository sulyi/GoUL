from abc import ABC
from collections.abc import Iterator

class GameBase(Iterator, ABC):
    def __init__(self, state):
        self._state = state

    @classmethod
    def name(cls):
        raise NotImplemented