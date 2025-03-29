from .game1 import Game1
from .game2 import Game2

def get_game_names():
    games = [Game1, Game2]
    return [game.name() for game in games]

default_game = Game1()

