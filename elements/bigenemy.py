import pygame
from spritesheet import Spritesheet
from elements.healthbar import HEALTHBAR

class BIGENEMY(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 210
        self.height = 200
        self.health = 100
        self.spritesheet = Spritesheet("assets/bigenemy/bigenemyanimation.png")
        self.stabsheet = Spritesheet("assets/bigenemy/stabbing.png")
        self.animation = []
        self.stabbing = []
        self.index = 0
        self.counter = 0
        self.speed = 6
        self.startposx =2000
        self.imune = False
        for num in range(0, 7):
            img = self.spritesheet.parse_sprite(f"New Piskel{num}.png").convert_alpha()
            img = pygame.transform.scale(img, (self.width, self.height))
            self.animation.append(img)
        self.image = self.animation[self.index]
        self.rect = self.image.get_rect(topleft=(self.startposx,1037-self.height))
        for num in range(0, 3):
            img = self.stabsheet.parse_sprite(f"New Piskel{num}.png").convert_alpha()
            img = pygame.transform.scale(img, (self.width, self.height))
            self.stabbing.append(img)

    def die(self):
        if self.health < 0:
            self.kill()

    def imunephase(self):
        if self.rect.x > 1579:
            self.imune = True
        else:
            self.imune = False

    def animate(self):
        speed = 10
        self.counter += 1
        if self.counter >= speed and self.index < len(self.animation):
            self.counter = 0
            self.index -= 1
        if self.index < 0:
            self.index = 6
        self.image = self.animation[self.index]

    def stab(self):
        self.speed = .1
        speed = 10
        self.counter += 1
        if self.counter >= speed and self.index < len(self.stabbing):
            self.counter = 0
            self.index += 1
        if self.index > len(self.stabbing)-1:
            self.index = 0
        self.image = self.stabbing[self.index]

    def move(self):
        self.startposx -= self.speed
        self.rect.x = self.startposx


    def update(self):
        self.imunephase()
        self.move()
        self.animate()
        self.die()
