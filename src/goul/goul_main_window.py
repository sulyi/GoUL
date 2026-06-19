import logging

from PyQt5.QtCore import QObject, QTimer, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget, QToolBar, QComboBox, QSizePolicy
from PyQt5.QtGui import QIcon

from .cellular_field import CellularField
from .games import get_game_names, from_game_name

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
matplot_logger = logging.getLogger('matplotlib.font_manager')


class GameClock(QObject):
    tick = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._timer = QTimer(self)
        self._timer.setInterval(10)
        self._timer.timeout.connect(self._on_timeout)

    def _on_timeout(self):
        self.tick.emit()

    @property
    def is_running(self):
        return self._timer.isActive()

    def start(self):
        if not self._timer.isActive():
            self._timer.start()

    def stop(self):
        if self._timer.isActive():
            self._timer.stop()


class GoULMainWindow(QMainWindow):
    game_types_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.game_clock = GameClock()
        self.game_clock.tick.connect(self._update_plot)

        self.cf = CellularField(None)

        games = get_game_names()

        self._create_toolbar(games)
        self.addToolBar(self.toolbar)

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
        if self.game_clock.is_running:
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

    def _create_toolbar(self, game_names):
        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setFixedHeight(40)

        self.step_action = self.toolbar.addAction(QIcon.fromTheme("edit-redo"), "")
        self.step_action.setToolTip("Step")
        self.step_action.triggered.connect(self.step_game)

        self.restart_action = self.toolbar.addAction(QIcon.fromTheme("view-refresh"), "")
        self.restart_action.setToolTip("Restart")
        self.restart_action.triggered.connect(self.generate_state)

        self.game_combo = QComboBox()
        self.game_combo.addItems(game_names)
        self.game_combo.currentTextChanged.connect(self.set_game_type)
        self.toolbar.addWidget(self.game_combo)

        # spacer to push play/stop to the right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar.addWidget(spacer)

        self.play_stop_toggle_action = self.toolbar.addAction(QIcon.fromTheme('media-playback-start'), "")
        self.play_stop_toggle_action.triggered.connect(self.toggle_run)

        if game_names:
            # ensure app state initialized
            self.game_combo.setCurrentIndex(0)
            self.set_game_type(self.game_combo.currentText())

        has_game = self.cf.game is not None
        self.step_action.setEnabled(has_game)
        self.play_stop_toggle_action.setEnabled(has_game)
        self.restart_action.setEnabled(has_game)

    def _cleanup(self):
        self._stop_game()

    def _update_plot(self):
        logger.debug("Updating plot...")
        try:
            next(self.cf.game)
            self._plot()
        except StopIteration as error:
            logger.warning("Game ended, due to: %s", error)
            self.game_clock.stop(break_loop=True)

    def _start_game(self):
        self.play_stop_toggle_action.setIcon(QIcon.fromTheme('media-playback-pause'))
        self.play_stop_toggle_action.setToolTip("Stop")
        logger.info("Starting game loop...")
        self.game_clock.start()

    def _stop_game(self):
        self.play_stop_toggle_action.setIcon(QIcon.fromTheme('media-playback-start'))
        self.play_stop_toggle_action.setToolTip("Play")
        logger.info("Stopping game loop...")
        self.game_clock.stop()

    def _plot(self):
        try:
            self.cf.plot()
        except ValueError as error:
            logger.warning("Game loop stopped, due to %s", error)
            self.game_clock.stop(break_loop=True)
