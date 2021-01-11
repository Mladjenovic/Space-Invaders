from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget

from Helpers.image_helper import get_image_path


class WindowHelper:

    @staticmethod
    def init_window(screen: QWidget, img: str):
        screen.background = QPixmap(get_image_path(img))
        screen.background_label = QtWidgets.QLabel(screen)
        screen.background_label.setPixmap(screen.background.scaled(1000, 600))
        screen.background_label.setGeometry(0, 0, 1000, 600)