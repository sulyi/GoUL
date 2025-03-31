from .game1 import Game1
from .game2 import Game2

_games = [Game1, Game2]

_game_lookup = {game.name(): game for game in _games}

def get_game_names():
    return [game.name() for game in _games]


def from_game_name(name, state=None):
        try:
            return _game_lookup[name](state)
        except KeyError as error:
            raise KeyError(f"No game named {name}") from error
