from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from .games.game_base import GameBase


class CellularField:

    def __init__(self, game: [GameBase, None]):
        self.game = game
        self._figure = Figure()
        self.canvas = FigureCanvas(self._figure)

    def plot(self):
        if not self.game:
            raise ValueError("Game is empty")

        self._figure.clear()

        if not self.game.state:
            self.canvas.draw()
            raise ValueError("Invalid game state")

        ax = self._figure.add_subplot(111)
        ax.axis(False)
        ax.matshow(self.game.state.data, **self.game.meta()['imshow'])
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

