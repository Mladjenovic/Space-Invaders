import copy
import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget

from Entities.Bullet import Bullet
from Entities.Box import Box
from Entities.Spaceship import Spaceship
from Factories.BulletFactory import BulletFactory
from Handlers.CollisionHandler import CollisionHandler


class BulletWorkerThread(QThread):
    update_bullet = pyqtSignal(Bullet)
    user_dead = pyqtSignal()
    update_lifes_number = pyqtSignal(int)

    def __init__(self, screen: QWidget, spaceship: Spaceship, enemies, score_label, score_list, box: Box, hearts: list):
        super().__init__()
        self.collisionHandler = CollisionHandler()
        self.enemies = enemies
        self.spaceship = spaceship
        self.screen = screen
        self.box = box
        self.hearts = hearts

        self.bullet = BulletFactory.create_object(self.screen, "bullet_id", self.spaceship.x + 22,
                                                  self.spaceship.y + 16 - 40,
                                                  "../Sources/Images/Player/player_laser.png", 6, 16, "player_id")

        self.score_list = score_list
        self.score_label = score_label

        self.allEnemies = []
        for e in enemies:
            self.allEnemies.append(e)

    def run(self):

        y = self.bullet.y
        while True:
            if y >= - 15:
                if self.collisionHandler._handleSpaceshipBulletWithEnemyCollision(self.bullet, self.enemies, self.allEnemies, self.score_label, self.score_list, self.screen):
                    break

                if self.collisionHandler._handleSpaceshipBulletWithBoxCollision(self.bullet, self.box, self.screen):
                    self.update_lifes_number.emit(self.box.luckyFactor)
                    break

                time.sleep(0.02)
                self.update_bullet.emit(self.bullet)
                y -= 15
            else:
                del self.bullet
                break
