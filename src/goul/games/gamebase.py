import abc

class GameBase(abc.ABC):
    @property
    def name(self):
        raise NotImplemented