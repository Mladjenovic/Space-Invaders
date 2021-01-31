from PyQt5.QtWidgets import QLabel, QWidget

from Entities.Box import Box
from Entities.Spaceship import Spaceship
from Network.SocketManager import SocketManager


class CollisionHandlerMultiplayer:

    @staticmethod
    def _handleSpaceshipWithEnemyBulletCollision(spaceship: Spaceship, enemy_bullets: list):
        for enemy_bullet in enemy_bullets:
            if (enemy_bullet.x < spaceship.x + 50) and (enemy_bullet.x >= spaceship.x) and (
                    enemy_bullet.y > spaceship.y) and (enemy_bullet.y < spaceship.y + 50):
                enemy_bullet.hide()
                enemy_bullets.remove(enemy_bullet)
                return True
            else:
                return False

    @staticmethod
    def _handleEnemyBulletWithShiledsCollision(shields: list, enemy_bullets: list):

        for shield in shields:

            for enemy_bullet in enemy_bullets:

                if (enemy_bullet.x < shield.x + 120) and (enemy_bullet.x >= shield.x) and (enemy_bullet.y > shield.y):
                    enemy_bullet.hide()
                    enemy_bullets.remove(enemy_bullet)
                    shield.shield_protection -= 1
                    shield.update_image()

                    if shield.shield_protection == 0:
                        shield.hide_shiled()
                        shields.remove(shield)

    def updateNumberOfLives(self, hearts: list, socketManager: SocketManager, playerUsername: str, myScore: int):

        if len(hearts) == 0:
            print("USER IS DEAD")
            socketManager.send_message(f"USER DIED|{playerUsername}|{myScore}")

            return True
        else:
            hearts[-1].hide()
            hearts.pop(-1)

            if len(hearts) == 0:
                print("USER IS DEAD")
                socketManager.send_message(f"USER DIED|{playerUsername}|{myScore}")
                return True

        return False

    @staticmethod
    def _handleSpaceshipBulletWithEnemyCollision(spaceship_bullet, enemies: list, allEnemies: list, score_label: QLabel,
                                                 score_list, screen: QWidget, socketManager: SocketManager,
                                                 spaceship_bullets, current_lvl, usernameScoreIndex: int):
        is_true = False

        for enemy in enemies:
            if (spaceship_bullet.x >= enemy.x) and (spaceship_bullet.x < enemy.x + 40) and \
                    (spaceship_bullet.y >= enemy.y) and (spaceship_bullet.y < enemy.y + 40):

                socketManager.send_message(f"ENEMY DIED|{enemy.object_id[0]}|{spaceship_bullet.object_id[0]}")

                spaceship_bullet.hide()
                spaceship_bullets.remove(spaceship_bullet)
                del spaceship_bullet

                enemy.hide()
                enemies.remove(enemy)

                if len(enemies) == 0:
                    current_lvl += 1
                    socketManager.send_message(f"NEW LEVEL|{str(current_lvl)}|")

                score_list[usernameScoreIndex] += enemy.value
                score_label.setText(f"SCORE: {score_list[usernameScoreIndex]}")
                socketManager.send_message(f"UPDATE SCORE|{usernameScoreIndex}|{enemy.value}")
                is_true = True
                break

        return is_true

    @staticmethod
    def _handleSpaceshipBulletWithEnemyCollisionRival(spaceship_bullet, enemies: list, allEnemies: list,
                                                      score_label: QLabel, score_list, screen: QWidget,
                                                      socketManager: SocketManager, spaceship_bullets):
        is_true = False

        for enemy in enemies:
            if (spaceship_bullet.x >= enemy.x) and (spaceship_bullet.x < enemy.x + 40) and \
                    (spaceship_bullet.y >= enemy.y) and (spaceship_bullet.y < enemy.y + 40):
                spaceship_bullet.hide()
                spaceship_bullets.remove(spaceship_bullet)
                del spaceship_bullet

                score_list[0] += enemy.value
                score_label.setText(f"SCORE: {score_list[0]}")
                print(score_list[0])
                is_true = True
                break

        return is_true

    @staticmethod
    def _handleSpaceshipBulletWithBoxCollision(spaceship_bullet, box: Box, screen: QWidget,
                                               socketManager: SocketManager):
        is_true = False

        if not box.isHidden:
            if (spaceship_bullet.x >= box.x) and (spaceship_bullet.x < box.x + 35) and \
                    (spaceship_bullet.y >= box.y) and (spaceship_bullet.y < box.y + 35):

                socketManager.send_message(f"HIT BOX||")

                spaceship_bullet.hide()
                del spaceship_bullet
                box.hide()
                box.isHidden = True

                if box.luckyFactor == -1:
                    print("GUBIS ZIVOT")
                else:
                    print("DOBIJAS ZIVOT")
                is_true = True

        return is_true


def check_level(level: int, enemies: list, allEnemies: list, screen: QWidget):
    if len(enemies) == 54:
        print('GOTOV LEVEL')
        enemies.clear()

        level += 1

        enemies = allEnemies
    return enemies
