import pygame
import pygame.sprite
from states.gameplay import *

from spritesheet import Spritesheet

class HEALTHBAR(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.healthbarimages = []
        self.spritesheet = Spritesheet("assets/bigenemy/healthbar.png")
        self.startposx = 2030
        self.speed = 6
        self.index = 0
        self.counter = 0
        for num in range(0, 10):
            img = self.spritesheet.parse_sprite(f"New Piskel{num}.png").convert_alpha()
            img = pygame.transform.scale(img, (100, 100))
            self.healthbarimages.append(img)
        self.image = self.healthbarimages[self.index]
        self.rect = self.image.get_rect(topleft=(self.startposx, 750))

    def move(self):
        self.startposx -= self.speed
        self.rect.x = self.startposx

    def update(self):
        self.move()
        try:
            self.image = self.healthbarimages[self.index]
        except:
            pass