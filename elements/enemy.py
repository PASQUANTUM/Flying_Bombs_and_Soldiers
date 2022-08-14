import pygame
import random
from spritesheet import Spritesheet
import os

class ENEMY(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.widthenemy = 100
        self.heightenemy = 100
        self.startposx = 1920
        self.speed = 8
        self.startposy = self.gettypeenemy()
        self.spritesheet = Spritesheet("assets/enemy/bomb.png")
        self.animation = []
        self.index = 0
        self.counter = 0
        for num in range (0,6):
            img = self.spritesheet.parse_sprite(f"New Piskel{num}.png").convert_alpha()
            img = pygame.transform.scale(img,(self.widthenemy,self.heightenemy))
            self.animation.append(img)
        self.image = self.animation[self.index]
        self.startpos = self.startposx, self.startposy
        self.rect = self.image.get_rect(bottomright = self.startpos)



    def move(self):
        self.startposx -= self.speed
        self.rect.x = self.startposx
        self.rect.y = self.startposy
        if self.rect.x < 0:
            self.startposx = 1920
            self.startposy = self.gettypeenemy()

    def gettypeenemy(self):
        rannum = random.randint(0,1)
        if rannum == 0:
            return 960
        else:
            return random.randint(830,850)

    def animate(self):
        speed = 4
        self.counter += 1
        if self.counter >= speed and self.index < len(self.animation) :
            self.counter = 0
            self.index += 1
        if self.index > 5:
            self.index = 0
        self.image = self.animation[self.index]

    def update(self):
        self.animate()
        self.move()