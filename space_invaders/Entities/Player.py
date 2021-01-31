# player_status: PlayerStatus=None

class Player:
    def __init__(self, player_id: str, username: str, lives_number: int, spaceship_id: str, score: int):
        self.player_id = player_id
        self.username = username
        self.lives_number = lives_number
        self.spaceship_id = spaceship_id
        self.score = score

    def decrease_lives_number(self):
        self.lives_number -= 1
        self.update_players_status()

    def update_players_status(self):
        pass

    def increase_score(self, earned_points: int):
        self.score += earned_points
        self.update_players_status()