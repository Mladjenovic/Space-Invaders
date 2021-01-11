from PyQt5.QtWidgets import QWidget

from Entities.MoveableObject import MoveableObject


class Enemy(MoveableObject):
    def __init__(self, screen: QWidget, enemy_id: str, x: int, y: int, img: str, width: int, height: int, value: int):
        super().__init__(screen=screen, object_id=enemy_id, x=x, y=y, img=img, width=width, height=height)
        self.value = value
