from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QMessageBox, QLabel

from Helpers.image_helper import get_image_path
from Network.Client.Client import Client
from Styles.ButtonStyles import button_style
from Styles.LabelStyles import player_username_label
from Styles.LineEditStyles import player_username_input


class MultiplayerMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 1000, 600)
        self.setFixedSize(1000, 600)
        self.setWindowTitle("Multiplayer")
        self.images = ["../Sources/Images/Player/red_spaceship.png", "../Sources/Images/Player/spaceship_blue.png", "../Sources/Images/Player/spaceship_yellow.png", "../Sources/Images/Player/spaceship_green.png"]
        self.selectedSpaceship = self.images[0]
        self.currentlySelected = 0

        self.init_UI()

    def init_UI(self):
        self.init_window()
        self.init_buttons()
        self.set_player_username()

    def init_buttons(self):
        self.connect_button = QtWidgets.QPushButton(self)
        self.connect_button.setText("Connect")
        self.connect_button.setGeometry(500, 100, 250, 50)
        self.connect_button.setStyleSheet(button_style)
        self.connect_button.clicked.connect(self.connect_button_function)

        self.host_button = QtWidgets.QPushButton(self)
        self.host_button.setText("Host")
        self.host_button.setGeometry(500, 200, 250, 50)
        self.host_button.setStyleSheet(button_style)
        self.host_button.clicked.connect(self.host_server)

        self.exit_button = QtWidgets.QPushButton(self)
        self.exit_button.setText("Exit")
        self.exit_button.setGeometry(500, 300, 250, 50)
        self.exit_button.setStyleSheet(button_style)
        self.exit_button.clicked.connect(self.exit)

        self.spaceship_label = QLabel(self)
        self.spaceship_label.resize(150, 150)
        self.spaceship_label.move(200, 320)

        self.spaceship_label.setStyleSheet("color: white;  font-size: 24px;")
        self.spaceship_label_image = self.selectedSpaceship
        self.spaceship_image_pixmap = QPixmap(get_image_path(self.spaceship_label_image))
        self.spaceship_label.setPixmap(self.spaceship_image_pixmap.scaled(self.spaceship_label.width(), self.spaceship_label.height()))
        self.spaceship_label.show()

        self.ipaddress_label = QLabel(self)
        self.ipaddress_label.setStyleSheet("color: white;  font-size: 22px;")
        self.ipaddress_label.resize(200, 50)
        self.ipaddress_label.setText("Servers IP Address: ")
        self.ipaddress_label.move(180, 460)
        self.ipaddress_label.show()

        self.ipaddress_input = QLineEdit(self)
        self.ipaddress_input.setGeometry(180, 510, 190, 50)
        self.ipaddress_input.setStyleSheet(player_username_input)

        #left button
        self.left_button = QtWidgets.QPushButton(self)
        self.left_button.setGeometry(140, 350, 50, 50)
        self.left_button.setText("<")
        self.left_button.setStyleSheet("border: 2px solid white; border-radius: 10px; color: white; font-size: 45px;  font-family: Times New Roman;")
        self.left_button.clicked.connect(self.change_left)
        self.left_button.show()


        #right button
        self.right_button = QtWidgets.QPushButton(self)
        self.right_button.setGeometry(360, 350, 50, 50)
        self.right_button.setText(">")
        self.right_button.setStyleSheet("border: 2px solid white; border-radius: 10px; color: white; font-size: 45px;  font-family: Times New Roman;")
        self.right_button.clicked.connect(self.change_right)
        self.right_button.show()

    def init_window(self):
        self.BackGround = QPixmap(get_image_path("../Sources/Images/Other/background.jpg"))

        self.BackGroundLabel = QtWidgets.QLabel(self)
        self.BackGroundLabel.setPixmap(self.BackGround.scaled(1000, 600))
        self.BackGroundLabel.resize(1000, 600)
        self.BackGroundLabel.setGeometry(0, 0, 1000, 600)

    def change_left(self):
        if self.currentlySelected == 0:
            self.currentlySelected = len(self.images) - 1
        else:
            self.currentlySelected -= 1

        self.selectedSpaceship = self.images[self.currentlySelected]
        self.spaceship_label_image = self.selectedSpaceship
        self.spaceship_image_pixmap = QPixmap(get_image_path(self.spaceship_label_image))
        self.spaceship_label.setPixmap(
        self.spaceship_image_pixmap.scaled(self.spaceship_label.width(), self.spaceship_label.height()))

    def change_right(self):
            if self.currentlySelected == len(self.images) - 1:
                self.currentlySelected = 0
            else:
                self.currentlySelected += 1

            self.selectedSpaceship = self.images[self.currentlySelected]
            self.spaceship_label_image = self.selectedSpaceship
            self.spaceship_image_pixmap = QPixmap(get_image_path(self.spaceship_label_image))
            self.spaceship_label.setPixmap(
            self.spaceship_image_pixmap.scaled(self.spaceship_label.width(), self.spaceship_label.height()))

    def exit(self):
        app = QApplication.instance()
        app.closeAllWindows()

    def connect_button_function(self):
        if self.player_username_input.text() == "":
            message = QMessageBox()
            message.setIcon(QMessageBox.NoIcon)
            message.setText("Please enter your username")
            message.setWindowTitle("Warning")
            message.exec_()
        elif self.ipaddress_input.text() == "":
            message = QMessageBox()
            message.setIcon(QMessageBox.NoIcon)
            message.setText("Please enter servers IP Address")
            message.setWindowTitle("Warning")
            message.exec_()
        else:
            self.hide()
            self.client = Client(self.player_username_input.text(), self.images[self.currentlySelected], self.ipaddress_input.text())
            self.client.show()
            '''
            self.game_loop = GameLoop(self.player_username_input.text())
            self.game_loop.show()
            self.hide()
            '''

    def set_player_username(self):
        self.player_username_label = QtWidgets.QLabel(self)
        self.player_username_label.setText("Enter your username")
        self.player_username_label.setGeometry(135, 100, 300, 50)
        self.player_username_label.setStyleSheet(player_username_label)

        self.player_username_input = QLineEdit(self)
        self.player_username_input.setGeometry(125, 200, 300, 40)
        self.player_username_input.setStyleSheet(player_username_input)

    def host_server(self):
        print("Dizanje servera")