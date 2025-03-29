import os
import logging
import sys

from PyQt5.QtCore import QUrl, QVariant, pyqtProperty, pyqtSignal, pyqtSlot
from PyQt5.QtQuick import QQuickView
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from .cellular_field import CellularField
from .games import default_game, get_game_names

logger = logging.getLogger()

class GoULMainWindow(QMainWindow):
    game_types_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.cf = CellularField(default_game)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Create the QQuickView for the QML toolbar
        toolbar_view = QQuickView()
        toolbar_view.setResizeMode(QQuickView.SizeRootObjectToView)
        context = toolbar_view.rootContext()
        context.setContextProperty("mainWindow", self)

        qml_file = os.path.join(os.path.dirname(__file__), 'toolbar.qml')
        toolbar_view.setSource(QUrl.fromLocalFile(os.path.abspath(qml_file)))
        status = toolbar_view.status()

        if status == QQuickView.Error:
            logger.error("Failed to load toolbar view")
            sys.exit(-1)

        # Wrap the QQuickView in a QWidget container
        toolbar = QWidget.createWindowContainer(toolbar_view)
        toolbar.setFixedHeight(40)  # Set a fixed height for the toolbar widget

        # Add the toolbar and canvas to the layout
        layout.addWidget(toolbar)
        layout.addWidget(self.cf.canvas)

        # Optional: Ensure the canvas takes the remaining space
        layout.setStretch(0, 0)  # Toolbar doesn't stretch
        layout.setStretch(1, 1)  # Canvas stretches to fill remaining space

        self.setCentralWidget(central_widget)

    @pyqtSlot()
    def update_plot(self):
        self.cf.update_plot()

    @pyqtSlot(str)
    def set_game_type(self, game_type):
        print(f"Selected game type: {game_type}")
        # Update the game type in your CellularField or Game class

    @pyqtProperty(QVariant, notify=game_types_changed)
    def game_type_names(self):
        return get_game_names()
