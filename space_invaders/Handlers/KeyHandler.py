from PyQt5.QtCore import Qt

from Factories.BulletFactory import BulletFactory


class KeyHandler:
    def __init__(self):
        super().__init__()
        print('1')

    @staticmethod
    def handle_key(screen, event, spaceship):
        key = event.key()

        if key == Qt.Key_Left:
            if spaceship.x == 0:
                pass
            else:
                spaceship.move(-5, 0)
        elif key == Qt.Key_Right:
            if spaceship.x == screen.width() - 50:
                pass
            else:
                spaceship.move(5, 0)
        elif key == Qt.Key_Space:
            bullet = BulletFactory.create_object(screen, "bullet_id", spaceship.x + 22, spaceship.y + 16 - 40,
                                                 "../Sources/Images/Player/player_laser.png", 6, 16, "player_id")
