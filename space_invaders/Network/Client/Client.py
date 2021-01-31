import socket
from multiprocessing import Queue

from PyQt5.QtWidgets import QMainWindow

from Network.Workers.BulletWorkerRivalWorkerMultiplayer import BulletWorkerRivalMultiplayerThread

'''---------------------------------------------------------------------------------------------------------------------'''
import multiprocessing as mp
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets
from Helpers.WindowHelper import WindowHelper
from Entities.Box import Box
from Entities.Bullet import Bullet
from Entities.Spaceship import Spaceship
from Network.Workers.BulletWorkerMultiplayer import BulletWorkerMultiplayerThread
from Network.Workers.DeusExMultiplayerWorker import DeusExMultiplayerWorkerThread
from Network.Workers.EnemiesWorkerMultiplayer import EnemiesWorkerMultiplayerThread
from Workers.KeyNotifier import KeyNotifierWorker
from Network.Workers.BulletEnemyWorkerMultiplayer import BulletEnemyWorkerMultiplayerThread
from Network.Handlers.CollisionHandlerMultiplayer import CollisionHandlerMultiplayer
from Styles.ButtonStyles import button_style
from Factories.EnemyFactory import EnemyFactory
from Factories.HeartFactory import HeartFactory
from Factories.ShieldFactory import ShieldFactory
from Factories.SpaceshipFactory import SpaceshipFactory
from Network.Workers.ListenThreadWorker import ListenThreadWorker
from Network.SocketManager import SocketManager

counter = 0
start_game = False
enemy_bullet_counter = 0
spaceship_bullet_counter = 0


def spaceshipShoot(self, spaceship: Spaceship, enemies, score_label, score_list, box: Box, hearts: list,
                   socketManager: SocketManager, spaceship_bullet_id, spaceship_bullets: list, current_lvl: int,
                   usernameScoreIndex: int):
    self.worker = BulletWorkerMultiplayerThread(self, spaceship, enemies, score_label, score_list, box, hearts,
                                                socketManager, spaceship_bullet_id, spaceship_bullets, current_lvl,
                                                usernameScoreIndex)
    self.worker.start()
    self.worker.finished.connect(bullet_finished)
    self.worker.update_lifes_number.connect(self.updateNumberOfLivesLuckyFactor)
    self.worker.update_bullet.connect(updateBullet)


def spaceshipShootRival(self, spaceship: Spaceship, enemies, score_label, score_list, box: Box, hearts: list,
                        socketManager: SocketManager, spaceship_bullet_id, spaceship_bullets: list):
    self.rivalWorker = BulletWorkerRivalMultiplayerThread(self, spaceship, enemies, score_label, score_list, box,
                                                          hearts,
                                                          socketManager, spaceship_bullet_id, spaceship_bullets)
    self.rivalWorker.start()
    self.rivalWorker.finished.connect(bullet_finished)
    self.rivalWorker.update_bullet_rival.connect(updateBulletRival)


def updateBulletRival(bullet: Bullet):
    bullet.move(0, -15)


def updateBullet(bullet: Bullet):
    bullet.move(0, -15)


def bullet_finished():
    print("Bullet removed and thread aborted")


class Client(QMainWindow):
    threads = []
    queue = Queue()

    def __init__(self, player_username, spaceship_image, server_ip_address):
        super().__init__()
        global spaceship_bullet_counter
        self.setGeometry(200, 200, 1000, 600)
        self.setFixedSize(1000, 600)
        self.setWindowTitle("GameLoop")
        self.all_spaceships = []
        self.enemies_coordinates = []
        self.spaceship_bullets = []
        self.score_labels = []
        self.score_list = []
        self.queue = Queue(maxsize=100)
        self.score_list.append(0)
        self.score_list.append(0)
        self.score_list.append(0)
        self.score_list.append(0)
        self.player_username = player_username
        self.spaceship_image = spaceship_image
        self.server_ip_address = server_ip_address
        self.collisionHandler = CollisionHandlerMultiplayer()
        self.ex_pipe, self.in_pipe = mp.Pipe()
        self.init_UI()
        self.initNetwork()

    def finishedWithEnemyBulletWorker(self):
        print("Thread used for enemies shooting aborted")

    def finishedWithMoveSpaceshipThread(self):
        print("Thread used for moving spaceship aborted")

    def finishedWithEnemiesWorker(self):
        print("Thread used for moving enemies aborted")

    def show_random_force(self, box: Box):
        print("Stiglo iz DeusExMultiplayerWorkera")
        print(box.x)
        print(box.y)
        self.box = box

    def updateEnemiesBullet(self, enemy_bullet: Bullet):
        if self.collisionHandler._handleSpaceshipWithEnemyBulletCollision(self.spaceship, self.enemy_bullets):
            isDead = self.collisionHandler.updateNumberOfLives(self.hearts, self.socketManager, self.player_username,
                                                               self.score_list[self.usernameScoreIndex])
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
                for label in self.score_labels:
                    label.hide()
                self.keyNotifierWorker.terminate()
                self.BulletEnemyWorkerMultiplayer.terminate()
                self.enemiesWorker.terminate()
                self.newBulletEnemyWorkerMultiplayer.terminate()
                self.DeusExMultiplayerWorker.terminate()

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
                self.finished_game_score_label.setText(f"Score: {self.score_list[self.usernameScoreIndex]}")
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
            isDead = self.collisionHandler.updateNumberOfLives(self.hearts, self.socketManager, self.player_username,
                                                               self.score_list[self.usernameScoreIndex])
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
                for label in self.score_labels:
                    label.hide()
                self.status_label.hide()
                self.level_label.hide()
                self.player_username_label.hide()
                self.keyNotifierWorker.terminate()
                self.BulletEnemyWorkerMultiplayer.terminate()
                self.enemiesWorker.terminate()
                self.newBulletEnemyWorkerMultiplayer.terminate()
                self.newBulletEnemyWorkerMultiplayer.terminate()

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
                self.finished_game_score_label.setText(f"Score: {self.score_list[self.usernameScoreIndex]}")
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
                if len(self.hearts) == 1:
                    heart = HeartFactory.create_object(self, "heart_id", 40, 560, "../Sources/Images/Player/life.png",
                                                       40,
                                                       40, "player_id")
                    self.hearts.append(heart)
                elif len(self.hearts) == 2:
                    heart = HeartFactory.create_object(self, "heart_id", 2 * 40, 560,
                                                       "../Sources/Images/Player/life.png", 40,
                                                       40, "player_id")
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
        self.BulletEnemyWorkerMultiplayer.terminate()
        self.enemiesWorker.terminate()
        self.newBulletEnemyWorkerMultiplayer.terminate()

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
        self.finished_game_score_label.setText(f"Score: {self.score_list[self.usernameScoreIndex]}")
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
            self.socketManager.send_message(f"MOVE LEFT|{self.spaceship.spaceship_id}|")
        elif key == Qt.Key_Right:
            self.spaceship.move_right(self)
            self.socketManager.send_message(f"MOVE RIGHT|{self.spaceship.spaceship_id}|")

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
        self.finished_winner_label.hide()
        app = QApplication.instance()
        app.closeAllWindows()

    def start_new_game(self):
        self.finished_game_label.hide()
        self.finished_game_score_label.hide()
        self.new_game_button.hide()
        self.finished_game_label.hide()
        self.exit_button.hide()
        self.finished_winner_label.hide()
        for spaceship in self.all_spaceships:
            spaceship.hide()
        self.score_list = []
        self.score_list.append(0)
        self.score_list.append(0)
        self.score_list.append(0)
        self.score_list.append(0)
        for label in self.score_labels:
            label.setText(f"SCORE: {0}")
        self.score_labels = []  # proveriti
        self.new_game_button.setEnabled(False)
        self.exit_button.setEnabled(False)
        self.socketManager.send_message(f"PLAY AGAIN|{self.spaceship.spaceship_id}|")

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
        self.spaceship = SpaceshipFactory.create_object(self, self.player_username, 475, 510,
                                                        f"{self.spaceship_image}", 50, 50, "player_id")
        self.finished_winner_label = QLabel(self)
        self.finished_winner_label.resize(360, 50)
        self.finished_winner_label.move(350, 450)

        self.finished_winner_label.setText("")
        self.finished_winner_label.setStyleSheet("color: white;  font-size: 25px;")
        self.finished_winner_label.show()
        condition = True
        for spaceship in self.all_spaceships:
            if self.spaceship.spaceship_id == spaceship.spaceship_id:
                condition = False
                break
        if condition:
            self.all_spaceships.append(self.spaceship)

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
        self.counter = 0
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
                # enemy = EnemyFactory.create_object(self, str(uuid.uuid1()), j * 85 - 70, i * 45 - 8, image, 40, 40, enemy_val)
                enemy = EnemyFactory.create_object(self, str(self.counter), j * 85 - 70, i * 45 - 8, image, 40, 40,
                                                   enemy_val)
                enemy.move(115, 20)
                self.enemies.append(enemy)
                self.counter += 1

    def set_statusbar(self):
        self.status_label = QLabel(self)
        self.status_label.setStyleSheet(
            "border :2px solid lime; border-left: 0px; border-right: 0px; border-bottom: 0px")
        self.status_label.resize(1000, 565)
        self.status_label.move(0, 565)
        self.status_label.show()
        self.player_username_label = QLabel(self)
        self.player_username_label.resize(260, 35)
        self.player_username_label.move(140, 562)
        self.player_username_label.setText("player: " + self.player_username)
        self.player_username_label.setStyleSheet("color: white;  font-size: 20px;")
        self.player_username_label.show()
        self.score_label_red = QLabel(self)
        self.score_label_red.resize(160, 40)
        self.score_label_red.move(300, 560)

        self.score_label_red.setText(f"SCORE: {self.score_list[0]}")
        self.score_label_red.setStyleSheet("color: red; font-size: 18px;")
        self.score_label_red.show()
        self.score_labels.append(self.score_label_red)
        self.score_label_blue = QLabel(self)
        self.score_label_blue.resize(160, 40)
        self.score_label_blue.move(450, 560)

        self.score_label_blue.setText(f"SCORE: {self.score_list[1]}")
        self.score_label_blue.setStyleSheet("color: blue; font-size: 18px;")
        self.score_label_blue.show()

        self.score_labels.append(self.score_label_blue)
        self.score_label_yellow = QLabel(self)
        self.score_label_yellow.resize(160, 40)
        self.score_label_yellow.move(600, 560)

        self.score_label_yellow.setText(f"SCORE: {self.score_list[2]}")
        self.score_label_yellow.setStyleSheet("color: yellow; font-size: 18px;")
        self.score_label_yellow.show()
        self.score_labels.append(self.score_label_yellow)
        self.score_label_green = QLabel(self)
        self.score_label_green.resize(160, 40)
        self.score_label_green.move(750, 560)

        self.score_label_green.setText(f"SCORE: {self.score_list[3]}")
        self.score_label_green.setStyleSheet("color: green; font-size: 18px;")
        self.score_label_green.show()
        self.score_labels.append(self.score_label_green)
        if "red" in self.spaceship_image:
            self.score_label = self.score_labels[0]
            self.usernameScoreIndex = 0
        elif "blue" in self.spaceship_image:
            self.score_label = self.score_labels[1]
            self.usernameScoreIndex = 1
        elif "yellow" in self.spaceship_image:
            self.score_label = self.score_labels[2]
            self.usernameScoreIndex = 2
        elif "green" in self.spaceship_image:
            self.score_label = self.score_labels[3]
            self.usernameScoreIndex = 3

        self.level_label = QLabel(self)
        self.level_label.resize(160, 40)
        self.level_label.move(900, 560)
        self.level_label.setText("LEVEL " + str(0))
        self.level_label.setStyleSheet("color: white;  font-size: 20px;")
        self.level_label.show()

    def keyPressEvent(self, event):
        global spaceship_bullet_counter
        if event.key() == Qt.Key_Space:
            self.socketManager.send_message(f"SHOOT|{self.spaceship.spaceship_id}|{spaceship_bullet_counter}")
            spaceshipShoot(self, self.spaceship, self.enemies, self.score_label, self.score_list, self.box, self.hearts,
                           self.socketManager, str(spaceship_bullet_counter), self.spaceship_bullets, self.level_num,
                           self.usernameScoreIndex)
            spaceship_bullet_counter += 1
        self.keyNotifierWorker.add_key(event.key())

    def keyReleaseEvent(self, event):
        self.keyNotifierWorker.rem_key(event.key())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.keyNotifierWorker.die()
            self.enemiesWorker.abort_thread()
            self.BulletEnemyWorkerMultiplayer.abort_enemy_shooting_thread()
            event.accept()
        else:
            event.ignore()

    def create_new_level(self, level_num: int):
        print('NOVI LEVEL')
        print(level_num)
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
            self.set_enemies()
            self.enemy_bullets = []
            self.set_shields()
            self.keyNotifierWorker.terminate()
            self.BulletEnemyWorkerMultiplayer.terminate()
            self.enemiesWorker.terminate()
            self.newBulletEnemyWorkerMultiplayer.terminate()
            self.DeusExMultiplayerWorker.terminate()
        self.keyNotifierWorker = KeyNotifierWorker()
        self.keyNotifierWorker.start()
        self.keyNotifierWorker.key_signal.connect(self.moveSpaceship)
        self.keyNotifierWorker.finished_signal.connect(self.finishedWithMoveSpaceshipThread)
        self.enemiesWorker = EnemiesWorkerMultiplayerThread(self.enemies, self.shields, self.level_num,
                                                            self.socketManager)
        self.enemiesWorker.start()
        self.enemiesWorker.finished_enemies_moving_signal.connect(self.finishedWithEnemiesWorker)
        self.enemiesWorker.update_enemies_position.connect(self.moveEnemies)
        self.enemiesWorker.new_level.connect(self.create_new_level)

        global enemy_bullet_counter
        self.BulletEnemyWorkerMultiplayer = BulletEnemyWorkerMultiplayerThread(self, self.enemies, self.enemy_bullets,
                                                                               self.level_num,
                                                                               str(enemy_bullet_counter))
        self.BulletEnemyWorkerMultiplayer.start()
        self.BulletEnemyWorkerMultiplayer.finish_enemy_shooting.connect(self.finishedWithEnemyBulletWorker)
        self.BulletEnemyWorkerMultiplayer.update_enemy_bullet.connect(self.updateEnemiesBullet)
        self.newBulletEnemyWorkerMultiplayer = BulletEnemyWorkerMultiplayerThread(self, self.enemies,
                                                                                  self.enemy_bullets, self.level_num,
                                                                                  str(enemy_bullet_counter))
        self.newBulletEnemyWorkerMultiplayer.start()
        self.newBulletEnemyWorkerMultiplayer.update_enemy_bullet.connect(self.updateEnemiesBulletHelper)
        self.DeusExMultiplayerWorker = DeusExMultiplayerWorkerThread(self, self.queue)
        self.DeusExMultiplayerWorker.start()
        self.DeusExMultiplayerWorker.show_random_force.connect(self.show_random_force)
        self.level_label.setText("LEVEL " + str(level_num))

    def initNetwork(self):
        self.connectSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connectSocket.connect((self.server_ip_address, 5000))
        print(self.server_ip_address)
        self.socketManager = SocketManager(self.connectSocket)
        message_to_send = f"NEW CLIENT|{self.player_username}|{self.spaceship_image}"
        self.socketManager.send_message(message_to_send)
        self.listen_thread = ListenThreadWorker(self.connectSocket, self.all_spaceships, self.queue)
        self.listen_thread.new_spaceship.connect(self.create_new_spaceship)
        self.listen_thread.start_game.connect(self.start_game)
        self.listen_thread.move_spaceship.connect(self.moving_spaceship_listen)
        self.listen_thread.spaceship_shoot.connect(self.spaceship_shoot_listen)
        self.listen_thread.start_another_game.connect(self.start_another_game_listen)
        self.listen_thread.remove_enemy.connect(self.remove_enemy_listen)
        self.listen_thread.create_new_level_listen.connect(self.create_new_level_listen_func)
        self.listen_thread.update_rival_score.connect(self.update_rival_score_listen)
        self.listen_thread.remove_spaceship.connect(self.remove_spaceship_listen)
        self.listen_thread.show_winner.connect(self.show_winner_listen)
        self.listen_thread.hide_lucky_box.connect(self.hide_lucky_box_listen)
        self.listen_thread.start()

    def create_new_spaceship(self, username, spaceship_image):
        global counter
        counter += 5
        if len(self.all_spaceships) == 0:
            spaceship = SpaceshipFactory.create_object(self, username, 475, 510,
                                                       f"{spaceship_image}", 50, 50, "player_id")
            self.all_spaceships.append(spaceship)
        for spaceship in self.all_spaceships:
            if not (spaceship.spaceship_id == username):
                spaceship = SpaceshipFactory.create_object(self, username, 475, 510,
                                                           f"{spaceship_image}", 50, 50, "player_id")
                self.all_spaceships.append(spaceship)

    def start_game(self):
        self.create_new_level(0)

    def moving_spaceship_listen(self, direction: str, spaceship_id: str):
        if direction == "MOVE LEFT":
            for spaceship in self.all_spaceships:
                if spaceship.spaceship_id == spaceship_id:
                    spaceship.move_left()
        elif direction == "MOVE RIGHT":
            for spaceship in self.all_spaceships:
                if spaceship.spaceship_id == spaceship_id:
                    spaceship.move_right(self)

    def spaceship_shoot_listen(self, spaceship_id: str, bullet_id: str):
        for spaceship in self.all_spaceships:
            if spaceship.spaceship_id == spaceship_id:
                spaceshipShootRival(self, spaceship, self.enemies, self.score_label, self.score_list, self.box,
                                    self.hearts,
                                    self.socketManager, bullet_id, self.spaceship_bullets)

    def start_another_game_listen(self):
        self.init_UI()
        for spaceship in self.all_spaceships:
            spaceship.x = 475
            spaceship.y = 510
            spaceship.label.move(spaceship.x, spaceship.y)
            if spaceship.spaceship_id != self.spaceship.spaceship_id:
                spaceship.show()
        self.create_new_level(self.level_num)

    def remove_enemy_listen(self, enemy_id: str, bullet_id: str):
        for enemy in self.enemies:
            if str(enemy.object_id[0]) == enemy_id:
                enemy.hide()
                self.enemies.remove(enemy)
        for bullet in self.spaceship_bullets:
            if str(bullet.object_id[0]) == bullet_id:
                bullet.hide()
                self.spaceship_bullets.remove(bullet)

        for enemy in self.enemies:
            print(enemy.object_id, end="")

    def create_new_level_listen_func(self, level: int):
        self.create_new_level(int(level))

    def update_rival_score_listen(self, scoreIndex: int, scoreValue: int):
        self.score_list[scoreIndex] += scoreValue
        self.score_labels[scoreIndex].setText(f"SCORE: {self.score_list[scoreIndex]}")

    def remove_spaceship_listen(self, spaceship_id: str):
        for spaceship in self.all_spaceships:
            if spaceship.spaceship_id == spaceship_id:
                spaceship.hide()

    def show_winner_listen(self, usernameOfWinner: str, winnerScore: int):
        print(f"POBEDNIK: usenrame={usernameOfWinner}, score = {winnerScore}")
        self.finished_winner_label.setText(f"Winner {usernameOfWinner} Score = {winnerScore}!")

    def hide_lucky_box_listen(self):
        self.box.hide()
        self.box.isHidden = True