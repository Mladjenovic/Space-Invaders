from PyQt5.QtCore import QThread, pyqtSignal
from Network.SocketManager import SocketManager
from queue import Queue


class ListenThreadWorker(QThread):
    new_spaceship = pyqtSignal(str, str)  # username, spaceship_image
    start_game = pyqtSignal()
    move_spaceship = pyqtSignal(str, str)
    spaceship_shoot = pyqtSignal(str, str)
    start_another_game = pyqtSignal()
    remove_enemy = pyqtSignal(str, str)
    create_new_level_listen = pyqtSignal(int)
    update_rival_score = pyqtSignal(int, int)
    remove_spaceship = pyqtSignal(str)
    show_winner = pyqtSignal(str, int)
    hide_lucky_box = pyqtSignal()

    def __init__(self, s, all_spaceships: list, queue: Queue):
        super().__init__()
        self.connectSocket = s
        self.socket_manager = SocketManager(s)
        self.all_spaceships = all_spaceships
        self.queue = queue

    def run(self):
        while True:
            try:
                flag, username, spaceship_image = self.socket_manager.recv_message()
                print(f"Primio sam od SERVERA: {flag}, {username}, {spaceship_image}")

                if flag == "NEW CLIENT":
                    self.new_spaceship.emit(username, spaceship_image)
                elif flag == "START GAME":
                    self.start_game.emit()
                elif flag == "MOVE LEFT":
                    self.move_spaceship.emit(flag, username)
                elif flag == "MOVE RIGHT":
                    self.move_spaceship.emit(flag, username)
                elif flag == "SHOOT":
                    self.spaceship_shoot.emit(username, spaceship_image)
                elif flag == "START ANOTHER GAME":
                    self.start_another_game.emit()
                elif flag == "REMOVE ENEMY":

                    spaceship_id = username
                    bullet_id = spaceship_image
                    self.remove_enemy.emit(spaceship_id, bullet_id)

                elif flag == "CREATE LEVEL":
                    level = username
                    self.create_new_level_listen.emit(int(level))

                elif flag == "UPDATE USER SCORE":
                    scoreIndex = username
                    scoreValue = spaceship_image
                    self.update_rival_score.emit(int(scoreIndex), int(scoreValue))
                elif flag == "REMOVE SPACESHIP":
                    self.remove_spaceship.emit(username)
                elif flag == "SHOW WINNER":
                    score = int(spaceship_image)
                    self.show_winner.emit(username, score)
                elif flag == "1" or flag == "-1":
                    luckyFactor = flag
                    x = username
                    y = spaceship_image
                    print(f"STIGLO IZ PROCESA {luckyFactor}, {x}, {y}")
                    self.queue.put([int(luckyFactor), int(x), int(y)])

                elif flag == "HIDE BOX":
                    self.hide_lucky_box.emit()

            except Exception as ex:
                print(f"Error {str(ex)}")
                break