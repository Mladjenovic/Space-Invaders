import multiprocessing as mp

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QApplication
from PyQt5.QtWidgets import QMessageBox

from Entities.Box import Box
from Entities.Bullet import Bullet
from Entities.Spaceship import Spaceship
from Factories.EnemyFactory import EnemyFactory
from Factories.HeartFactory import HeartFactory
from Factories.ShieldFactory import ShieldFactory
from Factories.SpaceshipFactory import SpaceshipFactory
from Handlers.CollisionHandler import CollisionHandler
from Helpers.WindowHelper import WindowHelper
from Styles.ButtonStyles import button_style
from Workers.BulletEnemyWorker import BulletEnemyWorkerThread
from Workers.BulletWorker import BulletWorkerThread
from Workers.DeusExProccess import DeusExProcess
from Workers.DeusExWorker import DeusExWorkerThread
from Workers.EnemiesWorker import EnemiesWorkerThread
from Workers.KeyNotifier import KeyNotifierWorker


def spaceshipShoot(self, spaceship: Spaceship, enemies, score_label, score_list, box: Box, hearts: list):
    self.worker = BulletWorkerThread(self, spaceship, enemies, score_label, score_list, box, hearts)
    self.worker.start()
    self.worker.finished.connect(bullet_finished)
    self.worker.update_lifes_number.connect(self.updateNumberOfLivesLuckyFactor)
    self.worker.update_bullet.connect(updateBullet)


def updateBullet(bullet: Bullet):
    bullet.move(0, -15)


def bullet_finished():
    print("Bullet removed and thread aborted")


class GameLoop(QWidget):
    def __init__(self, player_username):
        super().__init__()
        self.setGeometry(200, 200, 1000, 600)
        self.setFixedSize(1000, 600)
        self.setWindowTitle("GameLoop")

        self.player_username = player_username
        self.collisionHandler = CollisionHandler()

        self.ex_pipe, self.in_pipe = mp.Pipe()

        self.init_UI()

        self.create_new_level(0)

    def finishedWithEnemyBulletWorker(self):
        print("Thread used for enemies shooting aborted")

    def finishedWithMoveSpaceshipThread(self):
        print("Thread used for moving spaceship aborted")

    def finishedWithEnemiesWorker(self):
        print("Thread used for moving enemies aborted")

    def show_random_force(self, box: Box):
        print("Stiglo iz DeusExWorkera")
        print(box.x)
        print(box.y)
        self.box = box

    def updateEnemiesBullet(self, enemy_bullet: Bullet):

        if self.collisionHandler._handleSpaceshipWithEnemyBulletCollision(self.spaceship, self.enemy_bullets):
            isDead = self.collisionHandler.updateNumberOfLives(self.hearts)
            if isDead:
                for e in self.enemies:
                    e.hide()
                self.enemies.clear()

                for b in self.enemy_bullets:
                    b.hide()

                for s in self.shields:
                    s.hide_shiled()
                self.shields.clear()

                self.score_label.hide()
                self.status_label.hide()
                self.level_label.hide()
                self.player_username_label.hide()

                self.keyNotifierWorker.terminate()
                self.bulletEnemyWorker.terminate()
                self.enemiesWorker.terminate()
                self.newbulletEnemyWorker.terminate()
                self.DeusExWorker.terminate()
                self.process.terminate()

                self.spaceship.hide()

                self.finished_game_label = QLabel(self)
                self.finished_game_label.resize(360, 50)
                self.finished_game_label.move(400, 150)
                self.finished_game_label.setText(f"Player {self.player_username} died!")
                self.finished_game_label.setStyleSheet("color: white;  font-size: 32px;")
                self.finished_game_label.show()

                self.finished_game_score_label = QLabel(self)
                self.finished_game_score_label.resize(260, 50)
                self.finished_game_score_label.move(450, 200)
                self.finished_game_score_label.setText(f"Score: {self.score_list[0]}")
                self.finished_game_score_label.setStyleSheet("color: white;  font-size: 32px;")
                self.finished_game_score_label.show()

                self.new_game_button = QtWidgets.QPushButton(self)
                self.new_game_button.setText("New game")
                self.new_game_button.setGeometry(400, 280, 250, 50)
                self.new_game_button.setStyleSheet(button_style)
                self.new_game_button.clicked.connect(self.start_new_game)
                self.new_game_button.show()

                self.exit_button = QtWidgets.QPushButton(self)
                self.exit_button.setText("Exit")
                self.exit_button.setGeometry(400, 360, 250, 50)
                self.exit_button.setStyleSheet(button_style)
                self.exit_button.clicked.connect(self.exit)
                self.exit_button.show()

                self.new_game_button.setEnabled(True)
                self.exit_button.setEnabled(True)

        if self.collisionHandler._handleEnemyBulletWithShiledsCollision(self.shields, self.enemy_bullets):
            print("hitovan shield")

        if not enemy_bullet.isHidden:
            enemy_bullet.move(0, 6 + int(round(self.level_num / 2)))

    def updateEnemiesBulletHelper(self, enemy_bullet: Bullet):

        if self.collisionHandler._handleSpaceshipWithEnemyBulletCollision(self.spaceship, self.enemy_bullets):
            isDead = self.collisionHandler.updateNumberOfLives(self.hearts)
            if isDead:
                for e in self.enemies:
                    e.hide()
                self.enemies.clear()

                for b in self.enemy_bullets:
                    b.hide()

                for s in self.shields:
                    s.hide_shiled()
                self.shields.clear()

                self.score_label.hide()
                self.status_label.hide()
                self.level_label.hide()
                self.player_username_label.hide()

                self.keyNotifierWorker.terminate()
                self.bulletEnemyWorker.terminate()
                self.enemiesWorker.terminate()
                self.newbulletEnemyWorker.terminate()
                self.newbulletEnemyWorker.terminate()
                self.process.terminate()

                self.spaceship.hide()

                self.finished_game_label = QLabel(self)
                self.finished_game_label.resize(360, 50)
                self.finished_game_label.move(400, 150)
                self.finished_game_label.setText(f"Player {self.player_username} died!")
                self.finished_game_label.setStyleSheet("color: white;  font-size: 32px;")
                self.finished_game_label.show()

                self.finished_game_score_label = QLabel(self)
                self.finished_game_score_label.resize(260, 50)
                self.finished_game_score_label.move(450, 200)
                self.finished_game_score_label.setText(f"Score: {self.score_list[0]}")
                self.finished_game_score_label.setStyleSheet("color: white;  font-size: 32px;")
                self.finished_game_score_label.show()

                self.new_game_button = QtWidgets.QPushButton(self)
                self.new_game_button.setText("New game")
                self.new_game_button.setGeometry(400, 280, 250, 50)
                self.new_game_button.setStyleSheet(button_style)
                self.new_game_button.clicked.connect(self.start_new_game)
                self.new_game_button.show()

                self.exit_button = QtWidgets.QPushButton(self)
                self.exit_button.setText("Exit")
                self.exit_button.setGeometry(400, 360, 250, 50)
                self.exit_button.setStyleSheet(button_style)
                self.exit_button.clicked.connect(self.exit)
                self.exit_button.show()

                self.new_game_button.setEnabled(True)
                self.exit_button.setEnabled(True)

        if self.collisionHandler._handleEnemyBulletWithShiledsCollision(self.shields, self.enemy_bullets):
            print("hitovan shield")

        if not enemy_bullet.isHidden:
            enemy_bullet.move(0, 6 + int(round(self.level_num / 2)))

    def updateNumberOfLivesLuckyFactor(self, luckyFactor: int):
        if len(self.hearts) == 0:
            print("USER IS DEAD")
            self.user_died()
            return True
        else:

            if luckyFactor == 1:
                print("Treba da dodam novi zivot")

                if (len(self.hearts) == 1):
                    print("KREIRAM SRCULENCE")
                    heart = HeartFactory.create_object(self, "heart_id", 40, 560, "../Sources/Images/Player/life.png",
                                                       40,
                                                       40, "player_id")
                    print("KREIRANO SRCULENCE")
                    self.hearts.append(heart)
                elif len(self.hearts) == 2:
                    print("KREIRAM SRCULENCE")
                    heart = HeartFactory.create_object(self, "heart_id", 2 * 40, 560,
                                                       "../Sources/Images/Player/life.png", 40,
                                                       40, "player_id")
                    print("KREIRANO SRCULENCE")
                    self.hearts.append(heart)
            else:
                self.hearts[-1].hide()
                self.hearts.pop(-1)

                if len(self.hearts) == 0:
                    print("USER IS DEAD")
                    self.user_died()
                    return True

        return False

    def user_died(self):
        for e in self.enemies:
            e.hide()
        self.enemies.clear()

        for b in self.enemy_bullets:
            b.hide()

        for s in self.shields:
            s.hide_shiled()
        self.shields.clear()

        self.score_label.hide()
        self.status_label.hide()
        self.level_label.hide()
        self.player_username_label.hide()

        self.keyNotifierWorker.terminate()
        self.bulletEnemyWorker.terminate()
        self.enemiesWorker.terminate()
        self.newbulletEnemyWorker.terminate()
        self.process.terminate()

        self.spaceship.hide()

        self.finished_game_label = QLabel(self)
        self.finished_game_label.resize(360, 50)
        self.finished_game_label.move(400, 150)
        self.finished_game_label.setText(f"Player {self.player_username} died!")
        self.finished_game_label.setStyleSheet("color: white;  font-size: 32px;")
        self.finished_game_label.show()

        self.finished_game_score_label = QLabel(self)
        self.finished_game_score_label.resize(260, 50)
        self.finished_game_score_label.move(450, 200)
        self.finished_game_score_label.setText(f"Score: {self.score_list[0]}")
        self.finished_game_score_label.setStyleSheet("color: white;  font-size: 32px;")
        self.finished_game_score_label.show()

        self.new_game_button = QtWidgets.QPushButton(self)
        self.new_game_button.setText("New game")
        self.new_game_button.setGeometry(400, 280, 250, 50)
        self.new_game_button.setStyleSheet(button_style)
        self.new_game_button.clicked.connect(self.start_new_game)
        self.new_game_button.show()

        self.exit_button = QtWidgets.QPushButton(self)
        self.exit_button.setText("Exit")
        self.exit_button.setGeometry(400, 360, 250, 50)
        self.exit_button.setStyleSheet(button_style)
        self.exit_button.clicked.connect(self.exit)
        self.exit_button.show()

        self.new_game_button.setEnabled(True)
        self.exit_button.setEnabled(True)

    def moveSpaceship(self, key):

        if key == Qt.Key_Left:
            self.spaceship.move_left()
        elif key == Qt.Key_Right:
            self.spaceship.move_right(self)

    def moveEnemies(self, x, y):
        for i in range(len(self.enemies)):
            self.enemies[i].move(x, y)

    def newLevel(self, level):
        self.create_new_level(level)

    def exit(self):

        self.finished_game_label.hide()
        self.finished_game_score_label.hide()
        self.new_game_button.hide()
        self.exit_button.hide()

        app = QApplication.instance()
        app.closeAllWindows()

    def start_new_game(self):
        self.finished_game_label.hide()
        self.finished_game_score_label.hide()
        self.new_game_button.hide()
        self.exit_button.hide()

        self.new_game_button.setEnabled(False)
        self.exit_button.setEnabled(False)

        self.init_UI()
        self.create_new_level(0)

    def init_UI(self):
        WindowHelper.init_window(self, "../Sources/Images/Other/background.jpg")

        self.set_statusbar()
        self.set_hearts()
        self.set_shields()
        self.set_enemies()
        self.enemy_bullets = []

        self.box = Box(self, "box_id", 350, 350, "../Sources/Images/Other/box.png", 35, 35, "player_id")
        self.box.isHidden = True
        self.box.hide()

        self.level_num = 0

        self.spaceship = SpaceshipFactory.create_object(self, "ship_id", 475, 510,
                                                        "../Sources/Images/Player/player_ship.png", 50, 50, "player_id")

    def set_hearts(self):
        self.hearts = []
        for i in range(3):
            heart = HeartFactory.create_object(self, "heart_id", i * 40, 560, "../Sources/Images/Player/life.png", 40,
                                               40, "player_id")
            self.hearts.append(heart)

    def set_shields(self):
        self.shields = []
        for i in range(4):
            shield = ShieldFactory.create_object(self, "shiled_id", i * 265 + 40, 400,
                                                 "../Sources/Images/Shields/one.png", 120, 80, 9)

            self.shields.append(shield)

    def set_enemies(self):
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
                enemy = EnemyFactory.create_object(self, "enemy", j * 85 - 70, i * 45 - 8, image, 40, 40, enemy_val)
                enemy.move(115, 20)
                self.enemies.append(enemy)

    def set_statusbar(self):
        self.status_label = QLabel(self)
        self.status_label.setStyleSheet(
            "border :2px solid lime; border-left: 0px; border-right: 0px; border-bottom: 0px")
        self.status_label.resize(1000, 565)
        self.status_label.move(0, 565)
        self.status_label.show()

        self.player_username_label = QLabel(self)
        self.player_username_label.resize(260, 35)
        self.player_username_label.move(400, 562)
        self.player_username_label.setText("player: " + self.player_username)
        self.player_username_label.setStyleSheet("color: white;  font-size: 24px;")
        self.player_username_label.show()

        self.score_label = QLabel(self)
        self.score_label.resize(160, 40)
        self.score_label.move(840, 560)
        self.score_list = [0]
        self.score_label.setText(f"SCORE: {self.score_list[0]}")
        self.score_label.setStyleSheet("color: white; font-size: 24px;")
        self.score_label.show()

        self.level_label = QLabel(self)
        self.level_label.resize(160, 40)
        self.level_label.move(740, 560)
        self.level_label.setText("LEVEL " + str(0))
        self.level_label.setStyleSheet("color: white;  font-size: 24px;")
        self.level_label.show()


    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Space:
            spaceshipShoot(self, self.spaceship, self.enemies, self.score_label, self.score_list, self.box, self.hearts)

        self.keyNotifierWorker.add_key(event.key())

    def keyReleaseEvent(self, event):
        self.keyNotifierWorker.rem_key(event.key())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.keyNotifierWorker.die()
            self.enemiesWorker.abort_thread()
            self.bulletEnemyWorker.abort_enemy_shooting_thread()
            event.accept()
        else:
            event.ignore()

    def create_new_level(self, level_num: int):
        self.level_num = level_num

        if level_num != 0:

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
            self.process.terminate()
            self.DeusExWorker.terminate()

            self.set_enemies()
            self.enemy_bullets = []
            self.set_shields()

        self.keyNotifierWorker = KeyNotifierWorker()
        self.keyNotifierWorker.start()
        self.keyNotifierWorker.key_signal.connect(self.moveSpaceship)
        self.keyNotifierWorker.finished_signal.connect(self.finishedWithMoveSpaceshipThread)

        self.enemiesWorker = EnemiesWorkerThread(self.enemies, self.shields, self.level_num)
        self.enemiesWorker.start()
        self.enemiesWorker.finished_enemies_moving_signal.connect(self.finishedWithEnemiesWorker)
        self.enemiesWorker.update_enemies_position.connect(self.moveEnemies)
        self.enemiesWorker.new_level.connect(self.create_new_level)

        self.bulletEnemyWorker = BulletEnemyWorkerThread(self, self.enemies, self.enemy_bullets, self.level_num)
        self.bulletEnemyWorker.start()
        self.bulletEnemyWorker.finish_enemy_shooting.connect(self.finishedWithEnemyBulletWorker)
        self.bulletEnemyWorker.update_enemy_bullet.connect(self.updateEnemiesBullet)

        self.newbulletEnemyWorker = BulletEnemyWorkerThread(self, self.enemies, self.enemy_bullets, self.level_num)
        self.newbulletEnemyWorker.start()
        self.newbulletEnemyWorker.update_enemy_bullet.connect(self.updateEnemiesBulletHelper)

        self.process = DeusExProcess(pipe=self.ex_pipe, max_arg=101)
        self.process.start()

        self.DeusExWorker = DeusExWorkerThread(self, self.in_pipe)
        self.DeusExWorker.start()
        self.DeusExWorker.show_random_force.connect(self.show_random_force)

        self.level_label.setText("LEVEL " + str(level_num))