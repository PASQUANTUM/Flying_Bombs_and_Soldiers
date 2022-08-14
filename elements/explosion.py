import pygame
from spritesheet import Spritesheet

class Explosion(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 1000
        self.height = 1000
        self.images = []
        self.spritesheet = Spritesheet("assets/explosion.png")
        self.index = 0
        self.x, self.y = -200,500
        self.counter = 0
        for num in range(0, 5):
            img = self.spritesheet.parse_sprite(f"New Piskel{num}.png").convert_alpha()
            img = pygame.transform.scale(img, (self.width, self.height))
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        try:
            self.image = self.images[self.index]
        except:
            pass


