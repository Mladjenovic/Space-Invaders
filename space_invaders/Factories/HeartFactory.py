from PyQt5.QtWidgets import QWidget
from Entities.Heart import Heart


class HeartFactory:
    @staticmethod
    def create_object(screen: QWidget, heart_id: str, x: int, y: int, img: str, width: int, height: int, player_id: str):
        return Heart(screen=screen, heart_id=heart_id, x=x, y=y, img=img, width=width, height=height, player_id=player_id)