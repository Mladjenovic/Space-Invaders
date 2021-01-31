from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QMessageBox

from GUI.GameLoop import GameLoop
from Helpers.image_helper import get_image_path
from Styles.ButtonStyles import button_style
from Styles.LabelStyles import player_username_label
from Styles.LineEditStyles import player_username_input


class SinglePlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 1000, 600)
        self.setFixedSize(1000, 600)
        self.setWindowTitle("Single Player")
        self.init_UI()

    def init_UI(self):
        self.init_window()
        self.set_player_username()
        self.play_button()

    def init_window(self):
        self.background = QPixmap(get_image_path("../Sources/Images/Other/background.jpg"))
        self.background_label = QtWidgets.QLabel(self)
        self.background_label.setPixmap(self.background.scaled(1000, 600))
        self.background_label.setGeometry(0, 0, 1000, 600)

    def set_player_username(self):
        self.player_username_label = QtWidgets.QLabel(self)
        self.player_username_label.setText("Enter your username")
        self.player_username_label.setGeometry(385, 100, 300, 50)
        self.player_username_label.setStyleSheet(player_username_label)

        self.player_username_input = QLineEdit(self)
        self.player_username_input.setGeometry(375, 200, 300, 40)
        self.player_username_input.setStyleSheet(player_username_input)

    def play_button(self):
        self.play_button = QtWidgets.QPushButton(self)
        self.play_button.setText("Play")
        self.play_button.setGeometry(400, 350, 250, 50)
        self.play_button.setStyleSheet(button_style)
        self.play_button.clicked.connect(self.on_play_button_clicked)

    def on_play_button_clicked(self):
        if self.player_username_input.text() == "":
            message = QMessageBox()
            message.setIcon(QMessageBox.NoIcon)
            message.setText("Please enter your username")
            message.setWindowTitle("Warning")
            message.exec_()
        else:
             self.game_loop = GameLoop(self.player_username_input.text())
             self.game_loop.show()
             self.hide()