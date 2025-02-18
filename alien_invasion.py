import sys
import pygame
from ship import Ship
from bullet import Bullet
from settings import Settings

class AlienInvasionGame:
    def __init__(self):
        pygame.init()
        #Settings
        self.settings = Settings()
        # General
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption(self.settings.title_game)
        #Elements
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get(): 
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

    def _fire_bullet(self):
        #Create a new bullet and add to group of bullets
        if len(self.bullets) < self.settings.bullets_allowed: 
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.colors["dark"])
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        #Drawn the most recently screen visible
        pygame.display.flip()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()

if __name__ == '__main__':
    # Create instance of the game and play
    game = AlienInvasionGame()
    game.run_game() 

