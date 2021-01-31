from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel
from Helpers.image_helper import get_image_path


class Shield:
    def __init__(self, screen: QWidget, shield_id: str, x: int, y: int, img: str, width: int, height: int,
                 shield_protection: int):
        self.shield_id = shield_id
        self.x = x
        self.y = y
        self.img = img
        self.width = width
        self.height = height
        self.shield_protection = shield_protection

        self.isHidden = False

        self.label = QLabel(screen)
        self.label_image = self.img
        self.label_image_pixmap = QPixmap(get_image_path(self.label_image))
        self.label.setPixmap(self.label_image_pixmap.scaled(self.width, self.height))
        self.label.resize(self.width, self.height)
        self.label.move(self.x, self.y)

        self.label.show()

    def hide_shiled(self):
        self.isHidden = True
        self.label.hide()

    def changeLabelImage(self, img):
        self.label_image = img
        self.label_image_pixmap = QPixmap(get_image_path(self.label_image))
        self.label.setPixmap(self.label_image_pixmap.scaled(self.width, self.height))

    def update_image(self):
        print("shiled protection u update_image")
        print(self.shield_protection)

        if self.shield_protection >= 6 and self.shield_protection <= 9:
            pass
        elif self.shield_protection >= 3 and self.shield_protection <= 5:
            self.changeLabelImage("../Sources/Images/Shields/two.png")
            self.label.show()
        elif self.shield_protection >= 0 and self.shield_protection < 3:
            self.changeLabelImage("../Sources/Images/Shields/three.png")
            self.label.show()
        else:
            self.hide_shiled()
