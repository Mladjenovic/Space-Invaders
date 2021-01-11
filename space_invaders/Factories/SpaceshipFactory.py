from PyQt5.QtWidgets import QWidget

from Entities.Spaceship import Spaceship


class SpaceshipFactory:

    @staticmethod
    def create_object( screen: QWidget, spaceship_id: str,  x: int, y: int, img: str, width: int, height: int, player_id: str):
        return Spaceship(screen=screen, spaceship_id=spaceship_id, x=x, y=y, img=img, width=width, height=height, player_id=player_id)