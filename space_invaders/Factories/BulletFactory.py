from PyQt5.QtWidgets import QWidget

from Entities.Bullet import Bullet


class BulletFactory:

    @staticmethod
    def create_object(screen: QWidget, bullet_id: str,  x: int, y: int, img: str, width: int, height: int, player_id: str):
        return Bullet(screen=screen, bullet_id=bullet_id, x=x, y=y, img=img, width=width, height=height, player_id=player_id)