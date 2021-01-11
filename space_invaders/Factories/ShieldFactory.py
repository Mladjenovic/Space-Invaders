from PyQt5.QtWidgets import QWidget

from Entities.Shield import Shield


class ShieldFactory:

    @staticmethod
    def create_object(screen: QWidget, shield_id: str, x: int, y: int, img: str, width: int, height: int, shield_protection: int):
        return Shield(screen=screen, shield_id=shield_id, x=x, y=y, img=img, width=width, height=height, shield_protection=shield_protection)