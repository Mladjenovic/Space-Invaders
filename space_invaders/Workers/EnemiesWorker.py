import time

from PyQt5.QtCore import QThread, pyqtSignal


class EnemiesWorkerThread(QThread):
    new_level = pyqtSignal(int)
    update_enemies_position = pyqtSignal(int, int)
    finished_enemies_moving_signal = pyqtSignal()

    def __init__(self, enemies: list, shields: list, current_level: int):
        super().__init__()
        self.enemies = enemies
        self.is_done = False
        self.shields = shields
        self.current_level = current_level

    def __move_down__(self, enemies):

            all_can_move_down = True
            for enemy in enemies:
                if self.__can_move_down__(enemy, self.shields) is False:
                    all_can_move_down = False
            if all_can_move_down:
                time.sleep(0.75 - self.current_level * 0.03)
                self.update_enemies_position.emit(10, 3)

    def __moving_left__(self, enemies):
        while True:
            if len(self.enemies) == 0:
                print('PRAZNA LISTA')
                new_level_num = self.current_level+1

                self.new_level.emit(new_level_num)

            all_can_move_left = True
            for enemy in enemies:
                if self.__can_move_left__(enemy) is False:
                    all_can_move_left = False
                    self.__move_down__(self.enemies)
            if all_can_move_left:
                time.sleep(0.75 - self.current_level * 0.03)
                self.update_enemies_position.emit(-10 - int(round(self.current_level / 2)), 0)
            else:
                break

    def __moving_right__(self, enemies):

        while True:
            if len(self.enemies) == 0:
                new_level_num = self.current_level + 1
                self.new_level.emit(new_level_num)

            all_can_move_right = True
            for enemy in enemies:
                if self.__can_move_right__(enemy) is False:
                    all_can_move_right = False

            if all_can_move_right:
                time.sleep(0.75 - self.current_level * 0.03)
                self.update_enemies_position.emit(10 + int(round(self.current_level / 2)), 0)
            else:
                break

    @staticmethod
    def __can_move_left__(enemy):
        if enemy.x < 20:
            return False
        else:
            return True

    @staticmethod
    def __can_move_right__(enemy):
        if enemy.x > (1000 - 60):
            return False
        else:
            return True

    @staticmethod
    def __can_move_down__(enemy, shields):

        if len(shields) == 0:
            if enemy.y > 385:
                return False
            else:
                return True
        else:
            if enemy.y > 300:
                return False
            else:
                return True



    def abort_thread(self):
        """
        End notifications.
        """
        self.is_done = True
        self.enemies.clear()


        self.finished_enemies_moving_signal.emit()

    def run(self):
        while not self.is_done:
            self.__moving_left__(self.enemies)
            self.__moving_right__(self.enemies)