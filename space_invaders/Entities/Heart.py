from Entities.MoveableObject import MoveableObject
from PyQt5.QtWidgets import QWidget


class Heart(MoveableObject):
    def __init__(self, screen: QWidget, heart_id: str, x: int, y: int, img: str, width: int, height: int,
                 player_id: str):
        super().__init__(screen=screen, object_id=heart_id, x=x, y=y, img=img, width=width, height=height)
        self.player_id = player_id
