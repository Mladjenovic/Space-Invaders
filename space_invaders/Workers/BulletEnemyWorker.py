import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget

from Entities.Bullet import Bullet
from Entities.Spaceship import Spaceship
from Factories.BulletFactory import BulletFactory
from Entities.Enemy import Enemy
import random


class BulletEnemyWorkerThread(QThread):
    update_enemy_bullet = pyqtSignal(Bullet)
    finish_enemy_shooting = pyqtSignal()

    def __init__(self, screen: QWidget, enemies: list, enemy_bullets: list):
        super().__init__()

        self.enemies = enemies
        self.screen = screen
        self.enemy_bullets = enemy_bullets
        self.is_done = False


        self.random_enemy = random.choice(self.enemies)
        self.bullet = BulletFactory.create_object(self.screen, "bullet_0", self.random_enemy.x + 10,
                                                  self.random_enemy.y + 30,
                                                  "../Sources/Images/Enemy/enemy_laser.png", 6, 16, "player_id")

        self.enemy_bullets.append(self.bullet)

    def abort_enemy_shooting_thread(self):

        self.is_done = True
        self.finish_enemy_shooting.emit()

    def run(self):

        #time.sleep(3)
        y = self.bullet.y

        while not self.is_done:
            if y <= 600:
                time.sleep(0.04)
                self.update_enemy_bullet.emit(self.bullet)

                if (self.bullet.isHidden):
                    y = 700

                y += 6
            else:
                if (self.enemy_bullets.__contains__(self.bullet)):
                    self.enemy_bullets.remove(self.bullet)


                if len(self.enemies) != 0:
                    self.random_enemy = random.choice(self.enemies)
                    self.bullet.x = self.random_enemy.x + 10
                    self.bullet.y = self.random_enemy.y
                    y = self.bullet.y
                    self.bullet.show()
                    self.enemy_bullets.append(self.bullet)

