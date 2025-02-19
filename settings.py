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
        self.ship_speed = .5
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255,255,255)
        self.bullets_allowed = 3