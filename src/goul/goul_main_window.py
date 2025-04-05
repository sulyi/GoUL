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

    def stop(self):
        self.is_running = False
        self._thread.quit()
        self._thread.wait()

    def run(self):
        while self.is_running:
            self.game()

class GoULMainWindow(QMainWindow):
    game_types_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.game_loop = GameRunner(self.update_plot)

        container = QWidget()
        layout = QVBoxLayout(container)

        self.cf = CellularField(None)

        toolbar = self.create_toolbar()
        toolbar.setFixedHeight(40)

        layout.addWidget(toolbar)
        layout.addWidget(self.cf.canvas)
        self.setCentralWidget(container)

    @pyqtSlot()
    def update_plot(self):
        logger.info("Updating plot...")
        try:
            self.cf.update_plot()
        except ValueError as error:
            logging.warn(error)

    @pyqtSlot(str)
    def set_game_type(self, game_type):
        logger.info("Selected game type: %s", game_type)
        self.cf.game = from_game_name(
            game_type, self.cf.game.state if self.cf.game else None)
        self.update_plot()

    @pyqtSlot()
    def toggle_run(self):
        if self.game_loop.is_running:
            self.game_loop.stop()
        else:
            self.game_loop.start()

    @pyqtProperty(QVariant, notify=game_types_changed)
    def game_type_names(self):
        names = get_game_names()
        logger.info("Games: %s", names)
        return names

    def create_toolbar(self):
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

    def closeEvent(self, event):
        self.cleanup()
        event.accept()


    def cleanup(self):
        self.game_loop.stop()
