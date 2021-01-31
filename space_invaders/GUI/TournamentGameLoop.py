import time

import random
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets

import multiprocessing as mp

from Entities.Box import Box
from Entities.Bullet import Bullet
from Entities.Spaceship import Spaceship
from Entities.Enemy import Enemy

from Factories.EnemyFactory import EnemyFactory
from Factories.HeartFactory import HeartFactory
from Factories.ShieldFactory import ShieldFactory
from Factories.SpaceshipFactory import SpaceshipFactory
from Factories.BulletFactory import BulletFactory

from Helpers.WindowHelper import WindowHelper
from Styles.ButtonStyles import button_style

from Workers.BulletWorker import BulletWorkerThread
from Workers.DeusExProccess import DeusExProcess
from Workers.DeusExWorker import DeusExWorkerThread
from Workers.EnemiesWorker import EnemiesWorkerThread
from Workers.KeyNotifier import KeyNotifierWorker
from Workers.BulletEnemyWorker import BulletEnemyWorkerThread

from Handlers.CollisionHandler import CollisionHandler


def spaceshipShoot(self, spaceship: Spaceship, enemies, score1_label, score_list, box: Box, hearts: list):
    self.worker = BulletWorkerThread(self, spaceship, enemies, score1_label, score_list, box, hearts)
    self.worker.start()
    self.worker.finished.connect(bullet_finished)
    self.worker.update_lifes_number.connect(self.updateNumberOfLivesLuckyFactor)
    self.worker.update_bullet.connect(updateBullet)


def updateBullet(bullet: Bullet):
    bullet.move(0, -15)


def bullet_finished():
    print("Bullet removed and thread aborted")


class TournamentGameLoop(QWidget):
    def __init__(self, player1_username, player2_username, player3_username, player4_username,
                 player5_username, player6_username, player7_username, player8_username, ):
        super().__init__()
        self.setGeometry(200, 200, 1000, 600)
        self.setFixedSize(1000, 600)
        self.setWindowTitle("TournamentGameLoop")

        self.player1_username = player1_username
        self.player2_username = player2_username
        self.player3_username = player3_username
        self.player4_username = player4_username
        self.player5_username = player5_username
        self.player6_username = player6_username
        self.player7_username = player7_username
        self.player8_username = player8_username

        self.players_and_scores = {
            self.player1_username: [0],
            self.player2_username: [0],
            self.player3_username: [0],
            self.player4_username: [0],
            self.player5_username: [0],
            self.player6_username: [0],
            self.player7_username: [0],
            self.player8_username: [0]

        }

        self.current_players = {}
        self.waiting_players = {}
        self.winners = {}
        self.pair1 = {}
        self.pair2 = {}
        self.pair3 = {}
        self.pair4 = {}

        self.game_end = False

        self.choosePlayersRound1(self.players_and_scores)

        self.collisionHandler = CollisionHandler()

        self.ex_pipe, self.in_pipe = mp.Pipe()

        self.init_UI(self.current_players)

        self.create_new_level(0)

    def choosePlayersRound1(self, allPlayers):
        temp = {}

        for key, val in allPlayers.items():
            temp[key] = val

        player1 = key1, val1 = random.choice(list(temp.items()))
        temp.pop(key1)
        player2 = key2, val2 = random.choice(list(temp.items()))
        temp.pop(key2)
        self.pair1[key1] = val1
        self.pair1[key2] = val2

        player3 = key3, val3 = random.choice(list(temp.items()))
        temp.pop(key3)
        player4 = key4, val4 = random.choice(list(temp.items()))
        temp.pop(key4)
        self.pair2[key3] = val3
        self.pair2[key4] = val4

        player5 = key5, val5 = random.choice(list(temp.items()))
        temp.pop(key5)
        player6 = key6, val6 = random.choice(list(temp.items()))
        temp.pop(key6)
        self.pair3[key5] = val5
        self.pair3[key6] = val6

        player7 = key7, val7 = random.choice(list(temp.items()))
        temp.pop(key7)
        player8 = key8, val8 = random.choice(list(temp.items()))
        temp.pop(key8)
        self.pair4[key7] = val7
        self.pair4[key8] = val8

        self.current_players[key1] = val1
        self.current_players[key2] = val2
        self.waiting_players[key3] = val3
        self.waiting_players[key4] = val4
        self.waiting_players[key5] = val5
        self.waiting_players[key6] = val6
        self.waiting_players[key7] = val7

        self.waiting_players[key8] = val8

    def choosePlayersRound2(self, allPlayers):
        temp = {}

        for key, val in allPlayers.items():
            temp[key] = val

        player1 = key1, val1 = random.choice(list(temp.items()))
        temp.pop(key1)
        player2 = key2, val2 = random.choice(list(temp.items()))
        temp.pop(key2)
        self.pair1[key1] = val1
        self.pair1[key2] = val2

        player3 = key3, val3 = random.choice(list(temp.items()))
        temp.pop(key3)
        player4 = key4, val4 = random.choice(list(temp.items()))
        temp.pop(key4)
        self.pair2[key3] = val3
        self.pair2[key4] = val4

        self.current_players[key1] = val1
        self.current_players[key2] = val2
        self.waiting_players[key3] = val3
        self.waiting_players[key4] = val4

    def choosePlayersFinalRound(self, allPlayers):
        temp = {}

        for key, val in allPlayers.items():
            temp[key] = val

        player1 = key1, val1 = random.choice(list(temp.items()))
        temp.pop(key1)
        player2 = key2, val2 = random.choice(list(temp.items()))
        temp.pop(key2)
        self.pair1[key1] = val1
        self.pair1[key2] = val2

        self.current_players[key1] = val1
        self.current_players[key2] = val2


    def finishedWithEnemyBulletWorker(self):
        print("Thread used for enemies shooting aborted")

    def finishedWithMoveSpaceshipThread(self):
        print("Thread used for moving spaceship aborted")

    def finishedWithMoveSpaceshipThread2(self):
        print("Thread used for moving spaceship aborted")

    def finishedWithEnemiesWorker(self):
        print("Thread used for moving enemies aborted")

    def show_random_force(self, box: Box):
        print("Stiglo iz DeusExWorkera")
        print(box.x)
        print(box.y)
        self.box = box

    def updateEnemiesBullet(self, enemy_bullet: Bullet):

        if self.collisionHandler._handleSpaceshipWithEnemyBulletCollision(self.spaceship1, self.enemy_bullets):
            isDead = self.collisionHandler.updateNumberOfLives(self.hearts1)
            if isDead:
                for e in self.enemies:
                    e.hide()
                self.enemies.clear()

                for b in self.enemy_bullets:
                    b.hide()

                for s in self.shields:
                    s.hide_shiled()
                self.shields.clear()

                self.score1_label.hide()
                self.score2_label.hide()
                self.status_label.hide()
                self.level_label.hide()
                self.player1_username_label.hide()
                self.player2_username_label.hide()

                self.keyNotifierWorker.terminate()
                self.bulletEnemyWorker.terminate()
                self.enemiesWorker.terminate()
                self.newbulletEnemyWorker.terminate()
                self.DeusExWorker.terminate()
                self.process.terminate()

                self.spaceship1.hide()
                self.spaceship2.hide()
                for heart in self.hearts2:
                    heart.hide()

                for heart in self.hearts1:
                    heart.hide()

                self.box.hide()

                self.finished_game_label = QLabel(self)
                self.finished_game_label.resize(360, 50)
                self.finished_game_label.move(400, 150)
                self.finished_game_label.setStyleSheet("color: white;  font-size: 32px;")

                self.finished_game_score1_label = QLabel(self)
                self.finished_game_score1_label.resize(260, 50)
                self.finished_game_score1_label.move(400, 230)
                self.finished_game_score1_label.setText(f"{list(self.current_players.keys())[0]} Score: {self.score1_list[0]}")
                self.finished_game_score1_label.setStyleSheet("color: white;  font-size: 32px;")
                self.finished_game_score1_label.show()

                self.finished_game_score2_label = QLabel(self)
                self.finished_game_score2_label.resize(260, 50)
                self.finished_game_score2_label.move(400, 230)
                self.finished_game_score2_label.setText(f"{list(self.current_players.keys())[1]} Score: {self.score2_list[0]}")
                self.finished_game_score2_label.setStyleSheet("color: white;  font-size: 32px;")
                self.finished_game_score2_label.show()

                if not self.hearts1:
                    self.finished_game_label.setText(f"Player {list(self.current_players.keys())[0]} died!")
                    self.finished_game_label.show()
                    self.winners[list(self.current_players.keys())[1]] = [0]
                else:
                    self.finished_game_label.setText(f"Player {list(self.current_players.keys())[1]} died!")
                    self.finished_game_label.show()
                    self.winners[list(self.current_players.keys())[0]] = [0]


                self.current_players.clear()

                if self.pair1:
                    self.pair1.clear()

                if self.pair2:
                    for key, val in self.pair2.items():
                        self.current_players[key] = val
                    self.pair2.clear()
                elif self.pair3:
                    for key, val in self.pair3.items():
                        self.current_players[key] = val
                    self.pair3.clear()
                elif self.pair4:
                    for key, val in self.pair4.items():
                        self.current_players[key] = val
                    self.pair4.clear()
                else:
                    if len(self.winners.keys()) == 4:
                        # sledeca runda
                        self.choosePlayersRound2(self.winners)
                        self.winners.clear()
                        print("--------------------------------------\nRUNDA 2\n-----------------------------------")
                    elif len(self.winners.keys()) == 2:
                        # fianle
                        self.choosePlayersFinalRound(self.winners)
                        self.winners.clear()
                        print("--------------------------------------\nFINALE\n-----------------------------------")
                    else:
                        self.winner_game_label = QLabel(self)
                        self.winner_game_label.resize(360, 50)
                        self.winner_game_label.move(400, 50)
                        self.winner_game_label.setStyleSheet("color: white;  font-size: 32px;")
                        self.winner_game_label.setText(f"Player {list(self.winners.keys())[0]} wins!")
                        self.winner_game_label.show()
                        self.game_end = True

                if not self.game_end:
                    self.new_game_button = QtWidgets.QPushButton(self)
                    self.new_game_button.setText("Next")
                    self.new_game_button.setGeometry(400, 380, 250, 50)
                    self.new_game_button.setStyleSheet(button_style)
                    self.new_game_button.clicked.connect(self.start_new_game)
                    self.new_game_button.show()

                self.exit_button = QtWidgets.QPushButton(self)
                self.exit_button.setText("Exit")
                self.exit_button.setGeometry(400, 460, 250, 50)
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

        if self.collisionHandler._handleSpaceshipWithEnemyBulletCollision(self.spaceship1, self.enemy_bullets):
            isDead = self.collisionHandler.updateNumberOfLives(self.hearts1)
            if isDead:
                for e in self.enemies:
                    e.hide()
                self.enemies.clear()

                for b in self.enemy_bullets:
                    b.hide()

                for s in self.shields:
                    s.hide_shiled()
                self.shields.clear()

                self.score1_label.hide()
                self.score2_label.hide()
                self.status_label.hide()
                self.level_label.hide()
                self.player1_username_label.hide()
                self.player2_username_label.hide()

                self.keyNotifierWorker.terminate()
                self.bulletEnemyWorker.terminate()
                self.enemiesWorker.terminate()
                self.newbulletEnemyWorker.terminate()
                self.newbulletEnemyWorker.terminate()
                self.process.terminate()

                self.spaceship1.hide()
                self.spaceship2.hide()

                for heart in self.hearts2:
                    heart.hide()

                for heart in self.hearts1:
                    heart.hide()

                self.box.hide()

                self.finished_game_label = QLabel(self)
                self.finished_game_label.resize(360, 50)
                self.finished_game_label.move(400, 150)
                self.finished_game_label.setStyleSheet("color: white;  font-size: 32px;")

                self.finished_game_score1_label = QLabel(self)
                self.finished_game_score1_label.resize(260, 50)
                self.finished_game_score1_label.move(400, 230)
                self.finished_game_score1_label.setText(f"{list(self.current_players.keys())[0]} Score: {self.score1_list[0]}")
                self.finished_game_score1_label.setStyleSheet("color: white;  font-size: 32px;")
                self.finished_game_score1_label.show()

                self.finished_game_score2_label = QLabel(self)
                self.finished_game_score2_label.resize(260, 50)
                self.finished_game_score2_label.move(400, 285)
                self.finished_game_score2_label.setText(f"{list(self.current_players.keys())[1]} Score: {self.score2_list[0]}")
                self.finished_game_score2_label.setStyleSheet("color: white;  font-size: 32px;")
                self.finished_game_score2_label.show()

                if not self.hearts1:
                    self.finished_game_label.setText(f"Player {list(self.current_players.keys())[0]} died!")
                    self.finished_game_label.show()
                    self.winners[list(self.current_players.keys())[1]] = [0]
                else:
                    self.finished_game_label.setText(f"Player {list(self.current_players.keys())[1]} died!")
                    self.finished_game_label.show()
                    self.winners[list(self.current_players.keys())[0]] = [0]

                self.current_players.popitem()
                self.current_players.popitem()

                if self.pair1:
                    self.pair1.clear()

                if self.pair2:
                    for key, val in self.pair2.items():
                        self.current_players[key] = val
                    self.pair2.clear()
                elif self.pair3:
                    for key, val in self.pair3.items():
                        self.current_players[key] = val
                    self.pair3.clear()
                elif self.pair4:
                    for key, val in self.pair4.items():
                        self.current_players[key] = val
                    self.pair4.clear()
                else:
                    if len(self.winners.keys()) == 4:
                        # sledeca runda
                        self.choosePlayersRound2(self.winners)
                        self.winners.clear()
                        print("--------------------------------------\nRUNDA 2\n-----------------------------------")
                    elif len(self.winners.keys()) == 2:
                        # fianle
                        self.choosePlayersFinalRound(self.winners)
                        self.winners.clear()
                        print("--------------------------------------\nFINALE\n-----------------------------------")
                    else:
                        self.winner_game_label = QLabel(self)
                        self.winner_game_label.resize(360, 50)
                        self.winner_game_label.move(400, 50)
                        self.winner_game_label.setStyleSheet("color: white;  font-size: 32px;")
                        self.winner_game_label.setText(f"Player {list(self.winners.keys())[0]} wins!")
                        self.winner_game_label.show()
                        self.game_end = True

                if not self.game_end:
                    self.new_game_button = QtWidgets.QPushButton(self)
                    self.new_game_button.setText("Next")
                    self.new_game_button.setGeometry(400, 380, 250, 50)
                    self.new_game_button.setStyleSheet(button_style)
                    self.new_game_button.clicked.connect(self.start_new_game)
                    self.new_game_button.show()

                self.exit_button = QtWidgets.QPushButton(self)
                self.exit_button.setText("Exit")
                self.exit_button.setGeometry(400, 460, 250, 50)
                self.exit_button.setStyleSheet(button_style)
                self.exit_button.clicked.connect(self.exit)
                self.exit_button.show()

                self.new_game_button.setEnabled(True)
                self.exit_button.setEnabled(True)

        if self.collisionHandler._handleSpaceshipWithEnemyBulletCollision(self.spaceship2, self.enemy_bullets):
            isDead = self.collisionHandler.updateNumberOfLives(self.hearts2)
            if isDead:
                for e in self.enemies:
                    e.hide()
                self.enemies.clear()

                for b in self.enemy_bullets:
                    b.hide()

                for s in self.shields:
                    s.hide_shiled()
                self.shields.clear()

                self.score1_label.hide()
                self.score2_label.hide()
                self.status_label.hide()
                self.level_label.hide()
                self.player1_username_label.hide()
                self.player2_username_label.hide()

                self.keyNotifierWorker.terminate()
                self.bulletEnemyWorker.terminate()
                self.enemiesWorker.terminate()
                self.newbulletEnemyWorker.terminate()
                self.newbulletEnemyWorker.terminate()
                self.process.terminate()

                self.spaceship1.hide()
                self.spaceship2.hide()

                for heart in self.hearts2:
                    heart.hide()

                for heart in self.hearts1:
                    heart.hide()

                self.box.hide()

                self.finished_game_label = QLabel(self)
                self.finished_game_label.resize(360, 50)
                self.finished_game_label.move(400, 150)
                self.finished_game_label.setStyleSheet("color: white;  font-size: 32px;")

                self.finished_game_score1_label = QLabel(self)
                self.finished_game_score1_label.resize(260, 50)
                self.finished_game_score1_label.move(400, 230)
                self.finished_game_score1_label.setText(f"{list(self.current_players.keys())[0]} Score: {self.score1_list[0]}")
                self.finished_game_score1_label.setStyleSheet("color: white;  font-size: 32px;")
                self.finished_game_score1_label.show()

                self.finished_game_score2_label = QLabel(self)
                self.finished_game_score2_label.resize(260, 50)
                self.finished_game_score2_label.move(400, 285)
                self.finished_game_score2_label.setText(f"{list(self.current_players.keys())[1]} Score: {self.score2_list[0]}")
                self.finished_game_score2_label.setStyleSheet("color: white;  font-size: 32px;")
                self.finished_game_score2_label.show()

                if not self.hearts1:
                    self.finished_game_label.setText(f"Player {list(self.current_players.keys())[0]} died!")
                    self.finished_game_label.show()
                    self.winners[list(self.current_players.keys())[1]] = [0]
                else:
                    self.finished_game_label.setText(f"Player {list(self.current_players.keys())[1]} died!")
                    self.finished_game_label.show()
                    self.winners[list(self.current_players.keys())[0]] = [0]

                self.current_players.popitem()
                self.current_players.popitem()

                if self.pair1:
                    self.pair1.clear()

                if self.pair2:
                    for key, val in self.pair2.items():
                        self.current_players[key] = val
                    self.pair2.clear()
                elif self.pair3:
                    for key, val in self.pair3.items():
                        self.current_players[key] = val
                    self.pair3.clear()
                elif self.pair4:
                    for key, val in self.pair4.items():
                        self.current_players[key] = val
                    self.pair4.clear()
                else:
                    if len(self.winners.keys()) == 4:
                        # sledeca runda
                        self.choosePlayersRound2(self.winners)
                        self.winners.clear()
                        print("--------------------------------------\nRUNDA 2\n-----------------------------------")
                    elif len(self.winners.keys()) == 2:
                        # fianle
                        self.choosePlayersFinalRound(self.winners)
                        self.winners.clear()
                        print("--------------------------------------\nFINALE\n-----------------------------------")
                    else:
                        self.winner_game_label = QLabel(self)
                        self.winner_game_label.resize(360, 50)
                        self.winner_game_label.move(400, 50)
                        self.winner_game_label.setStyleSheet("color: white;  font-size: 32px;")
                        self.winner_game_label.setText(f"Player {list(self.winners.keys())[0]} wins!")
                        self.winner_game_label.show()
                        self.game_end = True

                if not self.game_end:
                    self.new_game_button = QtWidgets.QPushButton(self)
                    self.new_game_button.setText("Next")
                    self.new_game_button.setGeometry(400, 380, 250, 50)
                    self.new_game_button.setStyleSheet(button_style)
                    self.new_game_button.clicked.connect(self.start_new_game)
                    self.new_game_button.show()

                self.exit_button = QtWidgets.QPushButton(self)
                self.exit_button.setText("Exit")
                self.exit_button.setGeometry(400, 460, 250, 50)
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
        if len(self.hearts1) == 0:
            self.user_died()
            return True
        else:

            if luckyFactor == 1:
                if (len(self.hearts1) == 1):
                    heart = HeartFactory.create_object(self, "heart_id", 40, 560, "../Sources/Images/Player/life.png",
                                                       40,
                                                       40, "player_id")
                    self.hearts1.append(heart)
                elif len(self.hearts1) == 2:
                    heart = HeartFactory.create_object(self, "heart_id", 2 * 40, 560,
                                                       "../Sources/Images/Player/life.png", 40,
                                                       40, "player_id")
                    print("KREIRANO SRCULENCE")
                    self.hearts1.append(heart)
            else:
                self.hearts1[-1].hide()
                self.hearts1.pop(-1)

                if len(self.hearts1) == 0:
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

        self.score1_label.hide()
        self.score2_label.hide()
        self.status_label.hide()
        self.level_label.hide()
        self.player1_username_label.hide()
        self.player2_username_label.hide()

        self.keyNotifierWorker.terminate()
        self.bulletEnemyWorker.terminate()
        self.enemiesWorker.terminate()
        self.newbulletEnemyWorker.terminate()
        self.process.terminate()

        self.spaceship1.hide()
        self.spaceship2.hide()
        for heart in self.hearts2:
            heart.hide()

        for heart in self.hearts1:
            heart.hide()

        self.box.hide()

        self.finished_game_label = QLabel(self)
        self.finished_game_label.resize(360, 50)
        self.finished_game_label.move(400, 150)
        self.finished_game_label.setStyleSheet("color: white;  font-size: 32px;")

        self.finished_game_score1_label = QLabel(self)
        self.finished_game_score1_label.resize(260, 50)
        self.finished_game_score1_label.move(400, 230)
        self.finished_game_score1_label.setText(f"{list(self.current_players.keys())[0]} Score: {self.score1_list[0]}")
        self.finished_game_score1_label.setStyleSheet("color: white;  font-size: 32px;")
        self.finished_game_score1_label.show()

        self.finished_game_score2_label = QLabel(self)
        self.finished_game_score2_label.resize(260, 50)
        self.finished_game_score2_label.move(400, 230)
        self.finished_game_score2_label.setText(f"{list(self.current_players.keys())[1]} Score: {self.score2_list[0]}")
        self.finished_game_score2_label.setStyleSheet("color: white;  font-size: 32px;")
        self.finished_game_score2_label.show()

        if not self.hearts1:
            self.finished_game_label.setText(f"Player {list(self.current_players.keys())[0]} died!")
            self.finished_game_label.show()
            self.winners[list(self.current_players.keys())[1]] = [0]
        else:
            self.finished_game_label.setText(f"Player {list(self.current_players.keys())[1]} died!")
            self.finished_game_label.show()
            self.winners[list(self.current_players.keys())[0]] = [0]

        self.current_players.popitem()
        self.current_players.popitem()

        if self.pair1:
            self.pair1.clear()

        if self.pair2:
            for key, val in self.pair2.items():
                self.current_players[key] = val
            self.pair2.clear()
        elif self.pair3:
            for key, val in self.pair3.items():
                self.current_players[key] = val
            self.pair3.clear()
        elif self.pair4:
            for key, val in self.pair4.items():
                self.current_players[key] = val
            self.pair4.clear()
        else:
            if len(self.winners.keys()) == 4:
                # sledeca runda
                self.choosePlayersRound2(self.winners)
                self.winners.clear()
                print("--------------------------------------\nRUNDA 2\n-----------------------------------")

            elif len(self.winners.keys()) == 2:
                # fianle
                self.choosePlayersFinalRound(self.winners)
                self.winners.clear()
                print("--------------------------------------\nFINALE\n-----------------------------------")
            else:
                self.winner_game_label = QLabel(self)
                self.winner_game_label.resize(360, 50)
                self.winner_game_label.move(400, 50)
                self.winner_game_label.setStyleSheet("color: white;  font-size: 32px;")
                self.winner_game_label.setText(f"Player {list(self.winners.keys())[0]} wins!")
                self.winner_game_label.show()
                self.game_end = True

        if not self.game_end:
            self.new_game_button = QtWidgets.QPushButton(self)
            self.new_game_button.setText("Next")
            self.new_game_button.setGeometry(400, 380, 250, 50)
            self.new_game_button.setStyleSheet(button_style)
            self.new_game_button.clicked.connect(self.start_new_game)
            self.new_game_button.show()

        self.exit_button = QtWidgets.QPushButton(self)
        self.exit_button.setText("Exit")
        self.exit_button.setGeometry(400, 460, 250, 50)
        self.exit_button.setStyleSheet(button_style)
        self.exit_button.clicked.connect(self.exit)
        self.exit_button.show()

        self.new_game_button.setEnabled(True)
        self.exit_button.setEnabled(True)

    def moveSpaceship(self, key):

        if key == Qt.Key_Left:
            self.spaceship1.move_left()
        elif key == Qt.Key_Right:
            self.spaceship1.move_right(self)

    def moveSpaceship2(self, key):

        if key == Qt.Key_A:
            self.spaceship2.move_left()
        elif key == Qt.Key_D:
            self.spaceship2.move_right(self)

    def moveEnemies(self, x, y):
        for i in range(len(self.enemies)):
            self.enemies[i].move(x, y)

    def newLevel(self, level):
        self.create_new_level(level)

    def exit(self):

        self.finished_game_label.hide()
        self.finished_game_score1_label.hide()
        self.finished_game_score2_label.hide()
        self.new_game_button.hide()
        self.exit_button.hide()

        app = QApplication.instance()
        app.closeAllWindows()

    def start_new_game(self):
        self.finished_game_label.hide()
        self.finished_game_score1_label.hide()
        self.finished_game_score2_label.hide()
        self.new_game_button.hide()
        self.exit_button.hide()

        self.new_game_button.setEnabled(False)
        self.exit_button.setEnabled(False)

        self.init_UI(self.current_players)
        self.create_new_level(0)

    def init_UI(self, currentPlayers):
        WindowHelper.init_window(self, "../Sources/Images/Other/background.jpg")

        self.set_statusbar(currentPlayers)
        self.set_hearts(currentPlayers)
        self.set_shields()
        self.set_enemies()
        self.enemy_bullets = []

        self.box = Box(self, "box_id", 350, 350, "../Sources/Images/Other/box.png", 35, 35, "player_id")
        self.box.isHidden = True
        self.box.hide()

        self.level_num = 0

        self.spaceship1 = SpaceshipFactory.create_object(self, "ship1", 675, 510,
                                                         "../Sources/Images/Player/spaceship_blue.png", 50, 50,
                                                         list(currentPlayers.keys())[0])
        self.spaceship2 = SpaceshipFactory.create_object(self, "ship2", 275, 510,
                                                         "../Sources/Images/Player/spaceship_green.png", 50, 50,
                                                         list(currentPlayers.keys())[1])

    def set_hearts(self, currentPlayers):
        self.hearts1 = []
        for i in range(3):
            heart = HeartFactory.create_object(self, "heart_id", i * 40 + 880, 560, "../Sources/Images/Player/life.png",
                                               40,
                                               40, list(currentPlayers.keys())[0])
            self.hearts1.append(heart)

        self.hearts2 = []
        for i in range(3):
            heart = HeartFactory.create_object(self, "heart_id", i * 40, 560, "../Sources/Images/Player/life.png",
                                               40,
                                               40, list(currentPlayers.keys())[1])
            self.hearts2.append(heart)

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


    def set_statusbar(self, currentPlayers):
        self.status_label = QLabel(self)
        self.status_label.setStyleSheet(
            "border :2px solid lime; border-left: 0px; border-right: 0px; border-bottom: 0px")
        self.status_label.resize(1000, 565)
        self.status_label.move(0, 565)
        self.status_label.show()

        self.player1_username_label = QLabel(self)
        self.player1_username_label.resize(260, 35)
        self.player1_username_label.move(800, 562)
        self.player1_username_label.setText(list(currentPlayers.keys())[0])
        self.player1_username_label.setStyleSheet("color: white;  font-size: 24px;")
        self.player1_username_label.show()

        self.score1_label = QLabel(self)
        self.score1_label.resize(160, 40)
        self.score1_label.move(630, 560)
        self.score1_list = list(currentPlayers.values())[0]
        self.score1_label.setText(f"SCORE: {self.score1_list[0]}")
        self.score1_label.setStyleSheet("color: white; font-size: 24px;")
        self.score1_label.show()

        self.player2_username_label = QLabel(self)
        self.player2_username_label.resize(260, 35)
        self.player2_username_label.move(140, 562)
        self.player2_username_label.setText(list(currentPlayers.keys())[1])
        self.player2_username_label.setStyleSheet("color: white;  font-size: 24px;")
        self.player2_username_label.show()

        self.score2_label = QLabel(self)
        self.score2_label.resize(160, 40)
        self.score2_label.move(280, 560)
        self.score2_list = list(currentPlayers.values())[1]
        self.score2_label.setText(f"SCORE: {self.score2_list[0]}")
        self.score2_label.setStyleSheet("color: white; font-size: 24px;")
        self.score2_label.show()

        self.level_label = QLabel(self)
        self.level_label.resize(160, 40)
        self.level_label.move(440, 560)
        self.level_label.setText("LEVEL " + str(0))
        self.level_label.setStyleSheet("color: white;  font-size: 24px;")
        self.level_label.show()

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Delete:
            spaceshipShoot(self, self.spaceship1, self.enemies, self.score1_label, self.score1_list, self.box,
                           self.hearts1)

        if event.key() == Qt.Key_Space:
            spaceshipShoot(self, self.spaceship2, self.enemies, self.score2_label, self.score2_list, self.box,
                           self.hearts2)

        self.keyNotifierWorker.add_key(event.key())
        self.keyNotifierWorker2.add_key(event.key())

    def keyReleaseEvent(self, event):
        self.keyNotifierWorker.rem_key(event.key())
        self.keyNotifierWorker2.rem_key(event.key())

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
            self.keyNotifierWorker2.terminate()
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

        self.keyNotifierWorker2 = KeyNotifierWorker()
        self.keyNotifierWorker2.start()
        self.keyNotifierWorker2.key_signal.connect(self.moveSpaceship2)
        self.keyNotifierWorker2.finished_signal.connect(self.finishedWithMoveSpaceshipThread2)

        self.enemiesWorker = EnemiesWorkerThread(self.enemies, self.shields, self.level_num)
        self.enemiesWorker.start()
        self.enemiesWorker.finished_enemies_moving_signal.connect(self.finishedWithEnemiesWorker)
        self.enemiesWorker.update_enemies_position.connect(self.moveEnemies)
        self.enemiesWorker.new_level.connect(self.create_new_level)

        # testiranje

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