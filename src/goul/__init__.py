import argparse
import sys

from PyQt5.QtWidgets import QApplication

from .goul_main_window import GoULMainWindow, logger


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

    win = GoULMainWindow()
    win.show()

    sys.exit(app.exec())
