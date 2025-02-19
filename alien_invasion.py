import sys
import pygame
from ship import Ship
from bullet import Bullet
from ovni import Ovni
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
        self.ovnis = pygame.sprite.Group()
        self._create_fleet()

    def _check_events(self):
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
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

    def _create_fleet(self):
        ovni = Ovni(self)
        ovni_width, ovni_height = ovni.rect.size
        available_space_x = self.settings.screen_width - ( 2 * ovni_width)
        number_of_ovnis_x = available_space_x // (2 * ovni_width) 

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * ovni_height) - ship_height)
        number_rows = available_space_y // (2 * ovni_height)

        for row_number in range(number_rows):
            for ovni_number in range(number_of_ovnis_x):
                self._create_ovni(ovni_number, row_number)

    def _create_ovni(self, ovni_number, row_number):
        ovni = Ovni(self)
        ovni_width, ovni_height =  ovni.rect.size
        ovni.x = ovni_width + 2 * ovni_width * ovni_number
        ovni.rect.x = ovni.x
        ovni.rect.y  = ovni.rect.height + 2 * ovni.rect.height * row_number
        self.ovnis.add(ovni)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.colors["dark"])
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ovnis.draw(self.screen)
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

