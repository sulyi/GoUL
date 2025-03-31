from abc import ABC
from collections.abc import Iterator


class GameBase(Iterator, ABC):
    _meta = {'imshow': {'cmap': 'binary'}}
    _name = None

    # TODO: implement actual games:
    #  Conway's Game of Life
    #  Monte-Carlo Extension
    #  Point Process Extension

    def __init__(self, state):
        self.state = state if state is not None else self.get_init_state()

    @classmethod
    def name(cls):
        return cls._name

    @classmethod
    def meta(cls):
        return cls._meta

    def __next__(self):
        raise NotImplemented

    def get_init_state(self):
        raise NotImplemented
