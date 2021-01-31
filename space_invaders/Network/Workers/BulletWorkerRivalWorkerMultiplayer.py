import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget

from Entities.Box import Box
from Entities.Bullet import Bullet
from Entities.Spaceship import Spaceship
from Factories.BulletFactory import BulletFactory
from Network.Handlers.CollisionHandlerMultiplayer import CollisionHandlerMultiplayer
from Network.SocketManager import SocketManager


class BulletWorkerRivalMultiplayerThread(QThread):
    update_bullet_rival = pyqtSignal(Bullet)

    def __init__(self, screen: QWidget, spaceship: Spaceship, enemies, score_label, score_list, box: Box,
                 hearts: list, socketManager: SocketManager, spaceship_bullet_id: str, spaceship_bullets: list):
        super().__init__()
        self.collisionHandler = CollisionHandlerMultiplayer()
        self.enemies = enemies
        self.spaceship = spaceship
        self.screen = screen
        self.box = box
        self.hearts = hearts
        self.socketManager = socketManager
        self.spaceship_bullet_id = spaceship_bullet_id
        self.spaceship_bullets = spaceship_bullets

        self.bullet = BulletFactory.create_object(self.screen, f"{self.spaceship_bullet_id}", self.spaceship.x + 22,
                                                  self.spaceship.y + 16 - 40,
                                                  "../Sources/Images/Player/player_laser.png", 6, 16, "player_id")
        self.spaceship_bullets.append(self.bullet)

        self.score_list = score_list
        self.score_label = score_label

        self.allEnemies = []
        for e in enemies:
            self.allEnemies.append(e)

    def run(self):
        y = self.bullet.y
        while True:
            if y >= - 15:
                time.sleep(0.02)
                self.update_bullet_rival.emit(self.bullet)
                y -= 15

            else:
                del self.bullet
                break