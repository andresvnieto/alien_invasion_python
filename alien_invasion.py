import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from ovni import Ovni
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button

class AlienInvasionGame:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.title_game)
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.ovnis = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "Play")

    def _check_events(self):
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_ships()
            self.ovnis.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

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
        self._check_bullet_ovni_collitions()

    def _check_bullet_ovni_collitions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.ovnis, True, True)
        if collisions:
            for ovnis in collisions.values():
                self.stats.score += self.settings.game_points * len(ovnis)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()
        
        if not self.ovnis:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.scoreboard.prep_level()

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

    def _update_ovnis(self):
        self.check_fleet_edges()
        self.ovnis.update()
        if pygame.sprite.spritecollideany(self.ship, self.ovnis):
            self._ship_hit()
        self.check_ovnis_bottom()

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()

            ##Remainig bullets and ovnis
            self.ovnis.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            #Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def check_fleet_edges(self):
        for ovni in self.ovnis.sprites():
            if ovni.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        for ovni in self.ovnis.sprites():
            ovni.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def check_ovnis_bottom(self):
        screen_rect = self.screen.get_rect()
        for ovni in self.ovnis.sprites():
            if ovni.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.colors["dark"])
        self.ship.blitme()
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ovnis.draw(self.screen)
        self.scoreboard.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()
        
        pygame.display.flip()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_ovnis()

            self._update_screen() 

if __name__ == '__main__':
    # Create instance of the game and play
    game = AlienInvasionGame()
    game.run_game() 

