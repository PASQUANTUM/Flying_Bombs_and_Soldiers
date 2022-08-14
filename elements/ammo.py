import pygame
from spritesheet import Spritesheet

class AMMO(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.spritesheet = Spritesheet("assets/player/bullet.png")
        self.image = self.spritesheet.parse_sprite("New Piskel0.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(70,70))
        self.startposx = 2300
        self.startpos = self.startposx,1030
        self.rect = self.image.get_rect(bottomleft = self.startpos)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 8

    def move(self):
        self.startposx -= self.speed
        self.rect.x = self.startposx
        if self.rect.x < 0:
            self.startposx = 2300

    def update(self):
        self.move()
