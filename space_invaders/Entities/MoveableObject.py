from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from Helpers.image_helper import get_image_path


class MoveableObject:

    def __init__(self, screen: QWidget, object_id: str, x: int = 0, y: int = 0,
                 img: str = '', width: int = 0, height: int = 0):
        self.object_id = object_id,
        self.x = x
        self.y = y
        self.img = img
        self.width = width
        self.height = height
        self.isHidden = False

        self.label = QLabel(screen)
        self.label_image = self.img
        self.label_image_pixmap = QPixmap(get_image_path(self.label_image))
        self.label.setPixmap(self.label_image_pixmap.scaled(width, height))
        self.label.resize(self.width, self.height)
        self.label.move(self.x, self.y)

        self.label.show()

    def move(self, move_x: int, move_y: int):
        self.x = self.x + move_x
        self.y = self.y + move_y
        try:
            self.label.move(self.x, self.y)
        except Exception as e:
            print(str(e))

    def hide(self):
        self.isHidden = True
        self.label.hide()

    def show(self):
        self.isHidden = False
        self.label.show()

