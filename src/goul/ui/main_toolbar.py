from PyQt5.QtWidgets import QToolBar, QWidget, QComboBox, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal


class MainToolbar(QToolBar):
    game_type_changed = pyqtSignal(str)
    step_clicked = pyqtSignal()
    restart_clicked = pyqtSignal()
    play_pause_toggled = pyqtSignal()

    _TOOLBAR_HEIGHT = 40

    def __init__(self):
        super().__init__("Main Toolbar")
        self.setFixedHeight(self._TOOLBAR_HEIGHT)

        self.step_action = self.addAction(QIcon.fromTheme("edit-redo"), "")
        self.step_action.setToolTip("Step")
        self.step_action.triggered.connect(self.step_clicked.emit)

        self.restart_action = self.addAction(QIcon.fromTheme("view-refresh"), "")
        self.restart_action.setToolTip("Restart")
        self.restart_action.triggered.connect(self.restart_clicked.emit)

        self.game_combo = QComboBox()
        self.game_combo.currentTextChanged.connect(self.game_type_changed.emit)
        self.addWidget(self.game_combo)

        # spacer to push play/stop to the right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.addWidget(spacer)

        self.play_stop_toggle_action = self.addAction(QIcon.fromTheme('media-playback-start'), "")
        self.play_stop_toggle_action.triggered.connect(self.play_pause_toggled.emit)

    def set_playing(self, is_playing):
        if is_playing:
            self.play_stop_toggle_action.setIcon(QIcon.fromTheme('media-playback-pause'))
            self.play_stop_toggle_action.setToolTip("Stop")
        else:
            self.play_stop_toggle_action.setIcon(QIcon.fromTheme('media-playback-start'))
            self.play_stop_toggle_action.setToolTip("Play")

    def set_actions_enabled(self, enabled):
        self.step_action.setEnabled(enabled)
        self.play_stop_toggle_action.setEnabled(enabled)
        self.restart_action.setEnabled(enabled)
