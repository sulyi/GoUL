import argparse
import logging
import sys

from PyQt5.QtWidgets import QApplication

from .ui import MainWindow

# Configure logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
matplot_logger = logging.getLogger('matplotlib.font_manager')


def get_config(args):
    parser = argparse.ArgumentParser()
    log_levels = [
        "CRITICAL",
        "FATAL",
        "ERROR",
        "WARNING",
        "WARN",
        "INFO",
        "DEBUG",
        "NOTSET"
    ]
    parser.add_argument('-l', '--loglevel', default='WARN', choices=log_levels)

    return parser.parse_args(args[1:])


def main(args):
    app = QApplication(args)

    config = get_config(args)
    logger.setLevel(config.loglevel)
    matplot_logger.setLevel("WARNING")

    win = MainWindow()
    win.show()

    sys.exit(app.exec())
