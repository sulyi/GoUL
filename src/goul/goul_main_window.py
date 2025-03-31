import os
import logging
import random
import sys

from PyQt5.QtCore import QUrl, QVariant, pyqtProperty, pyqtSignal, pyqtSlot
from PyQt5.QtQuick import QQuickView
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from .cellular_field import CellularField
from .games import get_game_names, from_game_name

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())

class GoULMainWindow(QMainWindow):
    game_types_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        container = QWidget()
        self.layout = QVBoxLayout(container)

        self.cf = CellularField(None)

        toolbar = self.create_toolbar()
        toolbar.setFixedHeight(40)

        self.layout.addWidget(toolbar)
        self.layout.addWidget(self.cf.canvas)

        # layout.setStretch(0, 0)  # Toolbar doesn't stretch
        # layout.setStretch(1, 1)  # Canvas stretches to fill remaining space

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
        self.cf.game = from_game_name(game_type, self.cf.game.state if self.cf.game else None)
        self.cf.update_plot()

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
