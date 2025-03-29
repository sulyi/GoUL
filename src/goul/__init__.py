import sys

from PyQt5.QtWidgets import QApplication

from .main_window import GoULMainWindow


def main(args):
    app = QApplication(args)
    win = GoULMainWindow()
    win.show()
    sys.exit(app.exec())
