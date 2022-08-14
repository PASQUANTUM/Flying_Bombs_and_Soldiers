import pygame
from .base import BaseState
from spritesheet import Spritesheet


class Splash(BaseState):
    def __init__(self):
        super(Splash, self).__init__()
        self.myspritesheet0 = Spritesheet("assets/logo.png")
        self.startlogoanimations = []
        for num in range (0,31):
            img = self.myspritesheet0.parse_sprite(f"New Piskel{num}.png")
            img = pygame.transform.scale(img,(1920,1080))
            self.startlogoanimations.append(img)
        self.index = 0
        self.counter = 0
        self.next_state = "MENU"
        self.time_active = 0

    def update(self, dt):
        speed = 4
        self.counter += 1
        if self.counter >= speed and self.index < len(self.startlogoanimations)-1:
            self.counter = 0
            self.index += 1
        self.time_active += dt
        if self.time_active >= 2000:
            self.index = 0
        if self.time_active >= 2200:
            self.done = True

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.startlogoanimations[self.index],(425 ,1080/2-350))
