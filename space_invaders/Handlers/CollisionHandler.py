from Entities.Spaceship import Spaceship
from Entities.Bullet import Bullet
from PyQt5.QtWidgets import QLabel, QWidget

from Factories.EnemyFactory import EnemyFactory



class CollisionHandler:

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

        # if (enemy_bullet.x < spaceship.x + 50) and (enemy_bullet.x >= spaceship.x) and (enemy_bullet.y < spaceship.y + 50) and (enemy_bullet.y > spaceship.y - 50):

    @staticmethod
    def _handleEnemyBulletWithShiledsCollision(shields: list, enemy_bullets: list):

        for shield in shields:

            for enemy_bullet in enemy_bullets:

                if (enemy_bullet.x < shield.x + 120) and (enemy_bullet.x >= shield.x) and (enemy_bullet.y > shield.y):
                    enemy_bullet.hide()
                    enemy_bullets.remove(enemy_bullet)
                    shield.shield_protection -= 1
                    shield.update_image()

                    if (shield.shield_protection == 0):
                        shield.hide_shiled()
                        shields.remove(shield)

    def updateNumberOfLives(self, hearts: list):

        if len(hearts) == 0:
            print("USER IS DEAD")
        else:
            hearts[-1].hide()
            hearts.pop(-1)

            if len(hearts) == 0:
                print("USER IS DEAD")

    @staticmethod
    def _handleSpaceshipBulletWithEnemyCollision(spaceship_bullet, enemies: list, allEnemies: list, score_label: QLabel, score_list, screen: QWidget):
        is_true = False

        for enemy in enemies:
            if (spaceship_bullet.x >= enemy.x) and (spaceship_bullet.x < enemy.x + 40) and \
                    (spaceship_bullet.y >= enemy.y) and (spaceship_bullet.y < enemy.y + 40):

                spaceship_bullet.hide()
                del spaceship_bullet
                enemy.hide()
                enemies.remove(enemy)
                score_list[0] += enemy.value
                score_label.setText(f"SCORE: {score_list[0]}")
                print(score_list[0])
                is_true = True


                #enemies = check_level(1, enemies, allEnemies, screen)
                #print('DUZINAAAAAA')

                #print(len(enemies))
                #for e in enemies:
                 #   e.show()

                break

        return is_true



def check_level(level: int, enemies: list, allEnemies: list,  screen: QWidget):


    if len(enemies) == 54:
        print('GOTOV LEVEL')
        enemies.clear()

        level += 1

        enemies = allEnemies

        print('DUZINA ENEMIJA')
        print(len(enemies))


        print('POSLE KREIRANJA')

    return enemies
