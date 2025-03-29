import abc

class GameBase(abc.ABC):
    @classmethod
    def name(cls):
        raise NotImplemented