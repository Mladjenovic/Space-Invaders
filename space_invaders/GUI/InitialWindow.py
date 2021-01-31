from GUI.MultiplayerMenu import MultiplayerMenu
from Helpers.image_helper import get_image_path

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

from GUI.SinglePlayer import SinglePlayer
from GUI.Tournament import Tournament

import sys
from Styles.ButtonStyles import button_style


class InitialWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 1000, 600)
        self.setFixedSize(1000, 600)
        self.setWindowTitle("Menu")
        self.multiplayers = []

        self.init_UI()

    def init_UI(self):
        self.init_window()
        self.init_buttons()

    def init_buttons(self):
        self.singleplayer_button = QtWidgets.QPushButton(self)
        self.singleplayer_button.setText("Singleplayer")
        self.singleplayer_button.setGeometry(400, 100, 250, 50)
        self.singleplayer_button.setStyleSheet(button_style)
        self.singleplayer_button.clicked.connect(self.on_singleplayer_button)
        self.dialog = SinglePlayer()

        self.multiplayer_button = QtWidgets.QPushButton(self)
        self.multiplayer_button.setText("Multiplayer")
        self.multiplayer_button.setGeometry(400, 200, 250, 50)
        self.multiplayer_button.setStyleSheet(button_style)
        self.multiplayer_button.clicked.connect(self.on_mutliplayer_button)

        self.tournament_button = QtWidgets.QPushButton(self)
        self.tournament_button.setText("Tournament")
        self.tournament_button.setGeometry(400, 300, 250, 50)
        self.tournament_button.setStyleSheet(button_style)
        self.tournament_button.clicked.connect(self.on_tournament_button)
        self.dialog2 = Tournament()

        self.exit_button = QtWidgets.QPushButton(self)
        self.exit_button.setText("Exit")
        self.exit_button.setGeometry(400, 400, 250, 50)
        self.exit_button.setStyleSheet(button_style)
        self.exit_button.clicked.connect(self.exit)

    def init_window(self):
        self.BackGround = QPixmap(get_image_path("../Sources/Images/Other/background.jpg"))

        self.BackGroundLabel = QtWidgets.QLabel(self)
        self.BackGroundLabel.setPixmap(self.BackGround.scaled(1000, 600))
        self.BackGroundLabel.resize(1000, 600)
        self.BackGroundLabel.setGeometry(0, 0, 1000, 600)

    def exit(self):
        app = QApplication.instance()
        app.closeAllWindows()

    def on_singleplayer_button(self):
        self.hide()
        self.dialog.show()

    def on_mutliplayer_button(self):
        self.multiplayers.append(MultiplayerMenu())
        self.multiplayers[-1].show()

    def on_tournament_button(self):
        self.hide()
        self.dialog2.show()


def display_menu():
    app = QApplication(sys.argv)
    win = InitialWindow()

    win.show()
    sys.exit(app.exec_())