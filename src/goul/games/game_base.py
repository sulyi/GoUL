from abc import ABC
from collections.abc import Iterator

class GameBase(Iterator, ABC):
    _meta = {'imshow': {}}
    _name = None

    def __init__(self, state):
        self.state = state if state is not None else self.get_init_state()

    @classmethod
    def name(cls):
        return cls._name

    @classmethod
    def meta(cls):
        return cls._meta

    def get_init_state(self):
        raise NotImplemented
