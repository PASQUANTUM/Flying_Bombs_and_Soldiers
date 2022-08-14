import pygame
from spritesheet import Spritesheet

class BULLET(pygame.sprite.Sprite):
    def __init__(self,posx,posy):
        super().__init__()
        self.spritesheet = Spritesheet("assets/player/bullet.png")
        self.image = self.spritesheet.parse_sprite("New Piskel1.png")
        self.image = pygame.transform.scale(self.image,(25,25))
        self.rect = self.image.get_rect(center = (posx+175,posy-90))
        self.mask = pygame.mask.from_surface(self.image)
        self.bulletspeed = 24

    def update(self):
        self.rect.x += self.bulletspeed
        if self.rect.x > 1920:
            self.kill()



