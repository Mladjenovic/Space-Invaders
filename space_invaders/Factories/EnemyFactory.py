from PyQt5.QtWidgets import QWidget

from Entities.Enemy import Enemy


class EnemyFactory:

    @staticmethod
    def create_object(screen: QWidget, enemy_id: str, x: int, y: int, img: str, width: int, height: int, value: int):
        return Enemy(screen=screen, enemy_id=enemy_id, x=x, y=y, img=img, width=width, height=height, value=value)