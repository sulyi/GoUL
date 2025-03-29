from .game1 import Game1
from .game2 import Game2

def get_game_names():
    game_modules = [Game1, Game2]
    return [game_module.name for game_module in game_modules]

default_game = Game1()

