from PyQt5.QtWidgets import QWidget
from Entities.MoveableObject import MoveableObject


class Spaceship(MoveableObject):

    def __init__(self, screen: QWidget, spaceship_id: str, x: int, y: int,
                 img: str, width: int, height: int, player_id: str):

        super().__init__(screen=screen, object_id=spaceship_id, x=x, y=y,
                         img=img, width=width, height=height)
        self.spaceship_id = spaceship_id
        self.player_id = player_id

    def move_left(self):
        if self.x <= 0:
            pass
        else:
            self.move(-5, 0)

    def move_right(self, screen):
        if self.x == screen.width() - 50:
            pass
        else:
            self.move(5, 0)