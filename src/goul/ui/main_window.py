import logging

from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from .cellular_field import CellularField
from .main_toolbar import MainToolbar
from ..games import get_game_names, from_game_name

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    tick = pyqtSignal()
    _GAME_TICK_INTERVAL_MS = 10

    def __init__(self, parent=None):
        super().__init__(parent)

        self.game_clock = QTimer(self)
        self.game_clock.setInterval(self._GAME_TICK_INTERVAL_MS)
        self.game_clock.timeout.connect(self.tick.emit)
        self.tick.connect(self._update_plot)

        self.cf = CellularField(None)

        game_names = get_game_names()
        self.toolbar = MainToolbar()
        self.toolbar.game_combo.addItems(game_names)
        self.addToolBar(self.toolbar)

        self.toolbar.step_clicked.connect(self.step_game)
        self.toolbar.restart_clicked.connect(self.generate_state)
        self.toolbar.game_type_changed.connect(self.set_game_type)
        self.toolbar.play_pause_toggled.connect(self.toggle_run)

        # Initialize game state
        if game_names:
            self.set_game_type(self.toolbar.game_combo.currentText())

        self.setCentralWidget(self.cf.canvas)

    def step_game(self):
        logger.info("Stepping next state...")
        self._stop_game()
        self._update_plot()

    def set_game_type(self, game_type):
        logger.info("Selected game type: \"%s\"", game_type)
        self.cf.game = from_game_name(
            game_type, self.cf.game.state if self.cf.game else None)
        self._stop_game()
        self._plot()

    def toggle_run(self):
        if self.game_clock.isActive():
            self._stop_game()
        else:
            self._start_game()

    def generate_state(self):
        logger.info("Generating new state...")
        self._stop_game()
        self.cf.game.state = self.cf.game.get_init_state()
        self._plot()

    def closeEvent(self, event):
        self._cleanup()
        event.accept()

    def _cleanup(self):
        self._stop_game()

    def _update_plot(self):
        logger.debug("Updating plot...")
        try:
            next(self.cf.game)
            self._plot()
        except StopIteration as error:
            logger.warning("Game ended, due to: %s", error)
            self.game_clock.stop()

    def _start_game(self):
        self.toolbar.set_playing(True)
        logger.info("Starting game loop...")
        self.game_clock.start()

    def _stop_game(self):
        self.toolbar.set_playing(False)
        logger.info("Stopping game loop...")
        self.game_clock.stop()

    def _plot(self):
        try:
            self.cf.plot()
            self.toolbar.set_actions_enabled(self.cf.game is not None)
        except ValueError as error:
            logger.warning("Game loop stopped, due to %s", error)
            self.game_clock.stop()
