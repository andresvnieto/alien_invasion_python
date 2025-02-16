import sys

import pygame

class Settings:
    def __init__(self):
        self.titleGame = "Alien Invasion"
        # Colour Palette & Styling
        self.sizeWindow = (1200, 800)
        self.colors = {
            "white": (255,255,255),
            "purple": (94,40,162)
        }

class AlienInvasion:
    def __init__(self):
        pygame.init()
        #Settings
        self.settings = Settings()
        # General
        self.screen = pygame.display.set_mode(self.settings.sizeWindow)
        pygame.display.set_caption(self.settings.titleGame)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch keyboard events
            for event in pygame.event.get():
                # Escuha el evento de cerrar ventana
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.fill(self.settings.colors["purple"])
            pygame.display.flip()

if __name__ == '__main__':
    # Create instance of the game and play
    game = AlienInvasion()
    game.run_game() 