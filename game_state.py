
class Gamestats():
    def __init__(self,game_settings):
        self.game_settings = game_settings
        self.reset_state()
        self.game_active = False

    def reset_state(self):
        self.score = 0
        self.ship_left = self.game_settings.ship_limit