from abc import ABC
from collections.abc import Iterator

class GameBase(Iterator, ABC):
    def __init__(self, state):
        self.state = state if state is not None else self.get_init_state()

    @classmethod
    def name(cls):
        raise NotImplemented

    def get_init_state(self):
        raise NotImplemented
