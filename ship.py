import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, game):
        super().__init__()
        #Initilize the hship and start position
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings


        # Load the ship image and get its rect
        self.image = pygame.image.load('assets/space_ship.bmp')
        self.rect = self.image.get_rect()

        #Bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        
        #Movement Ship
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False

    def update(self):
        #Update position based on flag mobement
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        #Update x value
        self.rect.x = self.x 

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)
