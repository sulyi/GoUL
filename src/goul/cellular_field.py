from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from .games.game_base import GameBase


class CellularField:

    def __init__(self, game: [GameBase, None]):
        self.game = game
        self._figure = Figure()
        self.canvas = FigureCanvas(self._figure)

    def update_plot(self):
        if not self.game:
            raise ValueError("No game is set")

        state = next(self.game)

        self._figure.clear()
        ax = self._figure.add_subplot(111)
        ax.matshow(state.data, **self.game.meta()['imshow'])
        ax.axis(False)
        # Trigger the canvas to update and redraw.
        self.canvas.draw()
