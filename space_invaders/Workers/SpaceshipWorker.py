import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget

from Entities.Bullet import Bullet
from Entities.Spaceship import Spaceship


class SpaceshipWorkerThread(QThread):
    move_spaceship = pyqtSignal(Bullet)

    def __init__(self, screen: QWidget, spaceship: Spaceship):
        super().__init__()
        self.spaceship = spaceship
        self.screen = screen

    def run(self):

        x = self.spaceship.x

        while True:
            if y >= - 15:
                time.sleep(0.05)
                self.update_bullet.emit(self.bullet)
                y -= 15
            else:
                del self.bullet
                break
