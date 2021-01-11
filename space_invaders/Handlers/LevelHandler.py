from PyQt5.QtWidgets import QLabel, QWidget

from Workers.BulletWorker import BulletWorkerThread
from Workers.EnemiesWorker import EnemiesWorkerThread
from Workers.KeyNotifier import KeyNotifierWorker
from Workers.BulletEnemyWorker import BulletEnemyWorkerThread

from Factories.EnemyFactory import EnemyFactory
from Factories.HeartFactory import HeartFactory
from Factories.ShieldFactory import ShieldFactory
from Factories.SpaceshipFactory import SpaceshipFactory

class LevelHandler:

    def __init__(self, screen: QWidget, current_level: int, enemies: list, enemy_bullets: list, shields: list,
                 keyNotifierWorker: KeyNotifierWorker, enemiesWorker: EnemiesWorkerThread,
                 bulletEnemyWorker: BulletEnemyWorkerThread, newbulletEnemyWorker: BulletEnemyWorkerThread):
        print('kreiran level handler')
        self.current_level = current_level
        self.screen = screen
        self.enemies = enemies
        self.enemy_bullets = enemy_bullets
        self.shields = shields

        self.keyNotifierWorker = keyNotifierWorker
        self.enemiesWorker = enemiesWorker
        self.bulletEnemyWorker = bulletEnemyWorker
        self.newbulletEnemyWorker = newbulletEnemyWorker


    def create_new_level(current_level: int):

        print('NOVI LEVEL')

        if current_level != 0:

            for e in self.enemies:
                e.hide()
            self.enemies.clear()

            for b in self.enemy_bullets:
                b.hide()

            for s in self.shields:
                s.hide_shiled()
            self.shields.clear()

            self.keyNotifierWorker.terminate()
            self.bulletEnemyWorker.terminate()
            self.enemiesWorker.terminate()
            self.newbulletEnemyWorker.terminate()

            self.set_enemies(self.screen)
            self.enemy_bullets = []
            self.set_shields(self.screen)

        # self.keyNotifierWorker.die()
        # self.bulletEnemyWorker.abort_enemy_shooting_thread()
        # self.enemiesWorker.abort_thread()
        # self.newbulletEnemyWorker.abort_enemy_shooting_thread()



        #keyNotifierWorker = KeyNotifierWorker()
        self.keyNotifierWorker.start()
        self.keyNotifierWorker.key_signal.connect(self.screen.moveSpaceship)
        self.keyNotifierWorker.finished_signal.connect(self.screen.finishedWithMoveSpaceshipThread)

        #enemiesWorker = EnemiesWorkerThread(self.enemies, self.shields)
        self.enemiesWorker.start()
        self.enemiesWorker.finished_enemies_moving_signal.connect(self.screen.finishedWithEnemiesWorker)
        self.enemiesWorker.update_enemies_position.connect(self.screen.moveEnemies)
        self.enemiesWorker.new_level.connect(self.create_new_level)

        # testiranje

        #self.bulletEnemyWorker = BulletEnemyWorkerThread(self.screen, self.enemies, self.enemy_bullets)
        self.bulletEnemyWorker.start()
        self.bulletEnemyWorker.finish_enemy_shooting.connect(self.screen.finishedWithEnemyBulletWorker)
        self.bulletEnemyWorker.update_enemy_bullet.connect(self.screen.updateEnemiesBullet)

        #self.newbulletEnemyWorker = BulletEnemyWorkerThread(self.screen, self.enemies, self.enemy_bullets)
        self.newbulletEnemyWorker.start()
        # self.newbulletEnemyWorker.finish_enemy_shooting.connect(self.finishedWithEnemyBulletWorkerHelper)
        self.newbulletEnemyWorker.update_enemy_bullet.connect(self.screen.updateEnemiesBulletHelper)

    def set_hearts(self, screen: QWidget):
        self.hearts = []
        for i in range(3):
            heart = HeartFactory.create_object(screen, "heart_id", i * 40, 560, "../Sources/Images/Player/life.png", 40,
                                               40, "player_id")
            self.hearts.append(heart)
        return self.hearts

    def set_shields(self, screen: QWidget):
        self.shields = []
        for i in range(4):
            shield = ShieldFactory.create_object(screen, "shiled_id", i * 265 + 40, 400,
                                                 "../Sources/Images/Shields/one.png", 120, 80, 9)

            self.shields.append(shield)
        return self.shields

    def set_enemies(self, screen: QWidget):
        self.enemies = []
        enemy_val = 0
        for i in range(5):
            if i == 0:
                enemy_val = 200
                image = "../Sources/Images/Enemy/purple_enemy.png"
            elif i == 1 or i == 2:
                enemy_val = 100
                image = "../Sources/Images/Enemy/green_enemy.png"
            else:
                enemy_val = 50
                image = "../Sources/Images/Enemy/cyan_enemy.png"

            for j in range(11):
                enemy = EnemyFactory.create_object(screen, "enemy", j * 85 - 70, i * 45 - 8, image, 40, 40, enemy_val)
                enemy.move(115, 20)
                self.enemies.append(enemy)

        return self.enemies


    def set_statusbar(self, screen: QWidget):
        screen.status_label = QLabel(screen)
        screen.status_label.setStyleSheet(
            "border :2px solid lime; border-left: 0px; border-right: 0px; border-bottom: 0px")
        screen.status_label.resize(1000, 565)
        screen.status_label.move(0, 565)

        screen.player_username_label = QLabel(screen)
        screen.player_username_label.resize(260, 35)
        screen.player_username_label.move(400, 562)
        screen.player_username_label.setText("player: " + screen.player_username)
        screen.player_username_label.setStyleSheet("color: white;  font-size: 24px;")

        screen.score_label = QLabel(screen)
        screen.score_label.resize(160, 40)
        screen.score_label.move(840, 560)
        screen.score_list = [0]
        screen.score_label.setText(f"SCORE: {screen.score_list[0]}")
        screen.score_label.setStyleSheet("color: white; font-size: 24px;")
