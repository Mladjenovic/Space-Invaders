from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QMessageBox

from GUI.TournamentGameLoop import TournamentGameLoop
from Helpers.image_helper import get_image_path
from Styles.ButtonStyles import button_style
from Styles.LabelStyles import player_username_label
from Styles.LineEditStyles import player_username_input


class Tournament(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 1000, 600)
        self.setFixedSize(1000, 600)
        self.setWindowTitle("Tournament")
        self.init_UI()

    def init_UI(self):
        self.init_window()
        self.set_players()
        self.play_button()

    def init_window(self):
        self.background = QPixmap(get_image_path("../Sources/Images/Other/background.jpg"))
        self.background_label = QtWidgets.QLabel(self)
        self.background_label.setPixmap(self.background.scaled(1000, 600))
        self.background_label.setGeometry(0, 0, 1000, 600)

    def set_players(self):
        self.player1_username_label = QtWidgets.QLabel(self)
        self.player1_username_label.setText("Player 1")
        self.player1_username_label.setGeometry(10, 95, 300, 50)
        self.player1_username_label.setStyleSheet(player_username_label)

        self.player1_username_input = QLineEdit(self)
        self.player1_username_input.setGeometry(125, 100, 300, 40)
        self.player1_username_input.setStyleSheet(player_username_input)

        self.player2_username_label = QtWidgets.QLabel(self)
        self.player2_username_label.setText("Player 2")
        self.player2_username_label.setGeometry(10, 195, 300, 50)
        self.player2_username_label.setStyleSheet(player_username_label)

        self.player2_username_input = QLineEdit(self)
        self.player2_username_input.setGeometry(125, 200, 300, 40)
        self.player2_username_input.setStyleSheet(player_username_input)

        self.player3_username_label = QtWidgets.QLabel(self)
        self.player3_username_label.setText("Player 3")
        self.player3_username_label.setGeometry(10, 295, 300, 50)
        self.player3_username_label.setStyleSheet(player_username_label)

        self.player3_username_input = QLineEdit(self)
        self.player3_username_input.setGeometry(125, 300, 300, 40)
        self.player3_username_input.setStyleSheet(player_username_input)

        self.player4_username_label = QtWidgets.QLabel(self)
        self.player4_username_label.setText("Player 4")
        self.player4_username_label.setGeometry(10, 395, 300, 50)
        self.player4_username_label.setStyleSheet(player_username_label)

        self.player4_username_input = QLineEdit(self)
        self.player4_username_input.setGeometry(125, 400, 300, 40)
        self.player4_username_input.setStyleSheet(player_username_input)

        self.player5_username_label = QtWidgets.QLabel(self)
        self.player5_username_label.setText("Player 5")
        self.player5_username_label.setGeometry(510, 95, 300, 50)
        self.player5_username_label.setStyleSheet(player_username_label)

        self.player5_username_input = QLineEdit(self)
        self.player5_username_input.setGeometry(625, 100, 300, 40)
        self.player5_username_input.setStyleSheet(player_username_input)

        self.player6_username_label = QtWidgets.QLabel(self)
        self.player6_username_label.setText("Player 6")
        self.player6_username_label.setGeometry(510, 195, 300, 50)
        self.player6_username_label.setStyleSheet(player_username_label)

        self.player6_username_input = QLineEdit(self)
        self.player6_username_input.setGeometry(625, 200, 300, 40)
        self.player6_username_input.setStyleSheet(player_username_input)

        self.player7_username_label = QtWidgets.QLabel(self)
        self.player7_username_label.setText("Player 7")
        self.player7_username_label.setGeometry(510, 295, 300, 50)
        self.player7_username_label.setStyleSheet(player_username_label)

        self.player7_username_input = QLineEdit(self)
        self.player7_username_input.setGeometry(625, 300, 300, 40)
        self.player7_username_input.setStyleSheet(player_username_input)

        self.player8_username_label = QtWidgets.QLabel(self)
        self.player8_username_label.setText("Player 8")
        self.player8_username_label.setGeometry(510, 395, 300, 50)
        self.player8_username_label.setStyleSheet(player_username_label)

        self.player8_username_input = QLineEdit(self)
        self.player8_username_input.setGeometry(625, 400, 300, 40)
        self.player8_username_input.setStyleSheet(player_username_input)

    def play_button(self):
        self.play_button = QtWidgets.QPushButton(self)
        self.play_button.setText("Play")
        self.play_button.setGeometry(400, 500, 250, 50)
        self.play_button.setStyleSheet(button_style)
        self.play_button.clicked.connect(self.on_play_button_clicked)

    def on_play_button_clicked(self):
        if self.player1_username_input.text() == "" or self.player2_username_input.text() == "" or \
                self.player3_username_input.text() == "" or self.player4_username_input.text() == "":
            message = QMessageBox()
            message.setIcon(QMessageBox.NoIcon)
            message.setText("Please enter all players")
            message.setWindowTitle("Warning")
            message.exec_()
        else:
             self.game_loop = TournamentGameLoop(self.player1_username_input.text(), self.player2_username_input.text(),
                                                 self.player3_username_input.text(), self.player4_username_input.text(),
                                                 self.player5_username_input.text(), self.player6_username_input.text(),
                                                 self.player7_username_input.text(), self.player8_username_input.text())
             self.game_loop.show()
             self.hide()