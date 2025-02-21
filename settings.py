class Settings:
    def __init__(self):
        self.title_game = "Alien Invasion"
        # Colour Palette & Styling
        self.screen_width = 1200
        self.screen_height = 800
        self.size_window = (1200, 800)
        self.colors = {
            "white": (255,255,255),
            "dark": (36,37,86)
        }

        #Ship settings
        self.ship_speed = .5
        self.ship_limit = 3

        #bullet settings
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255,255,255)
        self.bullets_allowed = 3

        #Ovni settings
        self.ovni_speed = .3
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        self.speedup_scale = 1.1
        self.score_scale = 1.03
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 2.0
        self.ovni_speed = .2
        self.fleet_direction = 1
        self.game_points = 50
    
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.ovni_speed *= self.speedup_scale
        self.ovni_points = int(self.game_points * self.score_scale)