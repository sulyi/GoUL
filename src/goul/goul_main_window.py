import os
import logging
import sys

from PyQt5.QtCore import (
    QObject,
    QThread,
    QUrl,
    QVariant,
    pyqtProperty,
    pyqtSignal,
    pyqtSlot,
)
from PyQt5.QtQuick import QQuickView
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from .cellular_field import CellularField
from .games import get_game_names, from_game_name

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
matplot_logger = logging.getLogger('matplotlib.font_manager')


class GameRunner(QObject):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.is_running = False

        self._thread = QThread()
        self.moveToThread(self._thread)
        self._thread.started.connect(self.run)

    def start(self):
        self.is_running = True
        self._thread.start()

    def stop(self, break_loop=False):
        self.is_running = False
        self._thread.quit()
        if not break_loop:
            self._thread.wait()

    def run(self):
        while self.is_running:
            self.game()

class GoULMainWindow(QMainWindow):
    game_types_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.game_loop = GameRunner(self._update_plot)

        container = QWidget()
        layout = QVBoxLayout(container)

        self.cf = CellularField(None)

        toolbar = self._create_toolbar()
        toolbar.setFixedHeight(40)

        layout.addWidget(toolbar)
        layout.addWidget(self.cf.canvas)
        self.setCentralWidget(container)

    @pyqtSlot()
    def step_game(self):
        logger.info("Stepping next state...")
        self.game_loop.stop()
        self._update_plot()

    @pyqtSlot(str)
    def set_game_type(self, game_type):
        logger.info("Selected game type: \"%s\"", game_type)
        self.cf.game = from_game_name(
            game_type, self.cf.game.state if self.cf.game else None)
        self.game_loop.stop()
        self._plot()

    @pyqtSlot()
    def toggle_run(self):
        if self.game_loop.is_running:
            logger.info("Stopping game loop...")
            self.game_loop.stop()
        else:
            logger.info("Starting game loop...")
            self.game_loop.start()

    @pyqtSlot()
    def generate_state(self):
        logger.info("Generating new state...")
        self.game_loop.stop()
        self.cf.game.state = self.cf.game.get_init_state()
        self._plot()

    @pyqtProperty(QVariant, notify=game_types_changed)
    def game_type_names(self):
        names = get_game_names()
        logger.info("Games: %s", names)
        return names

    def closeEvent(self, event):
        self._cleanup()
        event.accept()

    def _create_toolbar(self):
        # Create the QQuickView for the QML toolbar
        toolbar_view = QQuickView()
        toolbar_view.rootContext().setContextProperty("toolbarCtx", self)

        qml_file = os.path.join(os.path.dirname(__file__), 'toolbar.qml')
        toolbar_view.setSource(QUrl.fromLocalFile(os.path.abspath(qml_file)))

        if toolbar_view.status() == QQuickView.Error:
            logger.error("Failed to load toolbar view")
            sys.exit(-1)

        toolbar_view.setResizeMode(QQuickView.SizeRootObjectToView)

        # Embed QQuickView into QWidget
        return QWidget.createWindowContainer(toolbar_view, self)

    def _cleanup(self):
        self.game_loop.stop()

    def _update_plot(self):
        logger.debug("Updating plot...")
        try:
            next(self.cf.game)
            self._plot()
        except StopIteration as error:
            logger.warning("Game ended, due to: %s", error)
            self.game_loop.stop(break_loop=True)

    def _plot(self):
        try:
            self.cf.plot()
        except ValueError as error:
            logger.warning("Game loop stopped, due to %s", error)
            self.game_loop.stop(break_loop=True)
