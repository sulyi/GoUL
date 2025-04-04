from .conways_game_of_life import DeterministicGame
from .game2 import Game2

_games = [DeterministicGame, Game2]
_game_lookup = {game.name(): game for game in _games}


def get_game_names():
    return [game.name() for game in _games]


def from_game_name(name, state=None):
    try:
        return _game_lookup[name](state)
    except KeyError as error:
        raise KeyError(f"No game named \"{name}\"") from error
