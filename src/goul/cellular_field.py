import random

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from .games.gamebase import GameBase


# TODO: Change placeholder graph to an actual animation that uses game to generate new data
class CellularField:
    n_data = 50
    xdata = list(range(n_data))

    def __init__(self, game: GameBase):
        self._data = [random.randint(0, 10) for i in range(self.n_data)]
        self._game = game
        self._figure = Figure()
        self.canvas = FigureCanvas(self._figure)
        self.update_plot()

    def update_plot(self):
        # Drop off the first y element, append a new one.
        self._data = self._data[1:] + [random.randint(0, 10)]
        self._figure.clear()
        ax = self._figure.add_subplot(111)
        ax.plot(self.xdata, self._data, 'r')
        # Trigger the canvas to update and redraw.
        self.canvas.draw()
