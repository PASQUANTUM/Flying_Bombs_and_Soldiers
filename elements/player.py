import pygame

from elements.bullet import BULLET
from spritesheet import Spritesheet


class PLAYER(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.widthplayer = 200
        self.heightplayer = 200
        self.spritesheet = Spritesheet("assets/player/basicanimation.png")
        self.spritesheetshoot = Spritesheet("assets/player/shootinganimation.png")
        self.spritesheetjump = Spritesheet("assets/player/jumpinganimation.png")
        self.image = self.spritesheet.parse_sprite("New Piskel0.png")
        self.slidingimage = pygame.image.load("assets/player/sliding.png")
        self.slidingimage = pygame.transform.scale(self.slidingimage, (self.widthplayer, self.heightplayer))
        self.image = pygame.transform.scale(self.image, (self.widthplayer, self.heightplayer))
        self.imagejump = self.spritesheetjump.parse_sprite("New Piskel3.png")
        self.imagejump = pygame.transform.scale(self.imagejump, (self.widthplayer, self.heightplayer))
        self.rect = self.image.get_rect(bottomleft=pos)
        self.shootanimation = []
        self.basicanimation = []
        self.crouchanimation = []
        self.crouching = False
        self.jumping = False
        self.jumpkey = False
        self.index = 0
        self.counter = 0
        self.posbulletx = pos[0]
        self.posbullety = pos[1]
        self.shooting = False
        self.ammunition = 30
        self.vel_y = 10

        for num in range(0, 2):
            img = self.spritesheetshoot.parse_sprite(f"New Piskel{num}.png")
            img = pygame.transform.scale(img, (self.widthplayer, self.heightplayer))
            self.shootanimation.append(img)

        for num in range(0, 4):
            img = self.spritesheet.parse_sprite(f"New Piskel{num}.png")
            img = pygame.transform.scale(img, (self.widthplayer, self.heightplayer))
            self.basicanimation.append(img)

    def jump(self):
        if self.jumping:
            self.rect.y -= self.vel_y * 2
            self.vel_y -= .5
            if self.vel_y < -10:
                self.jumping = False
                self.vel_y = 10

    def createbullet(self):
        return BULLET(self.posbulletx, self.posbullety)
