from Entities import Spaceship


class Storage:

    def __init__(self, enemies: list, enemies_bullets: list, shields: list, hearts: list, spaceship: Spaceship):
        self.enemies = enemies
        self.enemies_bullets = enemies_bullets
        self.shields = shields
        self.hearts = hearts
        self.spaceship = spaceship

    def get_enemies(self):
        return self.enemies

    def get_enemies_bullets(self):
        return self.enemies_bullets

    def get_shields(self):
        return self.shields

    def get_hearts(self):
        return self.hearts

    def get_spaceship(self):
        return self.spaceship
