from abc import ABC, abstractmethod
from collections.abc import Iterator


class GameBase(Iterator, ABC):
    _meta = {'imshow': {'cmap': 'binary'}}
    _name = None

    _DEFAULT_INITIAL_HEIGHT = 10
    _DEFAULT_INITIAL_WIDTH = 10

    _INITIAL_POP_SIZE = 0

    # TODO: implement actual games:
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

    @abstractmethod
    def __next__(self):
        ...

    @abstractmethod
    def get_init_state(
            self,
            height=_DEFAULT_INITIAL_HEIGHT,
            width=_DEFAULT_INITIAL_WIDTH
    ):
        ...
