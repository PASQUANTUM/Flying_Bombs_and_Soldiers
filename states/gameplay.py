from os import path

import pygame
import random
from elements.ammo import AMMO
from elements.bigenemy import BIGENEMY
from elements.enemy import ENEMY
from elements.player import PLAYER
from .base import BaseState
from elements.healthbar import HEALTHBAR
from elements.bullet import BULLET
from elements.explosion import Explosion

class Gameplay(BaseState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.next_state = "GAME_OVER"
        self.x, self.y = 100, 1030
        self.playersprite = PLAYER((self.x, self.y))
        self.bigenemy = BIGENEMY()
        self.bigenemysprites = []
        self.bigenemysprites.append(self.bigenemy)
        self.bottomrect = pygame.Rect((0, 1030), (1920, 50))
        self.bottomimage = pygame.image.load('assets/background/floor.png').convert_alpha()
        self.enemysprite = ENEMY()
        self.ammosprite = AMMO()
        self.healthbar = HEALTHBAR()
        self.healthbarlist = []
        self.healthbarlist.append(self.healthbar)
        self.displayedimage = self.playersprite.image
        self.displayedrect = self.playersprite.rect
        self.highscore = self.load_data()
        self.points = 0
        self.explosion = Explosion()
        self.scoretext = f"SCORE: {self.points}"
        self.scoresurf = self.font.render(self.scoretext, True, "red")
        self.nhstext = "NEW HIGHSCORE!"
        self.nhssurf = self.font.render(self.nhstext, True, "red")
        self.ammotext = f"AMMO:{self.playersprite.ammunition}"
        self.ammosurf = self.font.render(self.ammotext, True, "red")
        self.bulletgroup = pygame.sprite.Group()
        self.time_active = 0
        self.exploding = False
        self.stabbing = False

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL and not self.stabbing:
                self.playersprite.crouching = True
            elif event.key == pygame.K_SPACE and not self.stabbing:
                self.playersprite.jumping = True
            elif event.key == pygame.K_q and self.playersprite.ammunition != 0:
                self.playersprite.shooting = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.done = True
            elif event.key == pygame.K_LCTRL:
                self.playersprite.crouching = False
            elif event.key == pygame.K_q:
                self.playersprite.shooting = False

    def draw(self, surface):
        surface.fill(pygame.Color("white"))
        surface.blit(self.bottomimage,(self.bottomrect))
        surface.blit(self.displayedimage, (self.displayedrect))
        surface.blit(self.enemysprite.image, (self.enemysprite.rect))
        surface.blit(self.ammosprite.image, (self.ammosprite.rect))
        self.bulletgroup.draw(surface)
        surface.blit(self.scoresurf, (0, 0))
        surface.blit(self.ammosurf, (0, 1000))
        if self.points > self.highscore: surface.blit(self.nhssurf, (1920 / 2 - 100, 1080 / 2))
        for hb in self.healthbarlist:
            surface.blit(hb.image,(hb.rect))
        for be in self.bigenemysprites:
            surface.blit(be.image,(be.rect))
        if self.exploding is True:
            surface.blit(self.explosion.image,(self.explosion.rect))

    def lost(self):
        self.healthbar.speed = 6
        self.bigenemy.speed = 6
        new_x_shift = random.randint(0, 1000)
        self.bigenemysprites.pop()
        self.bigenemysprites.append(self.bigenemy)
        self.bigenemy.startposx = 2000
        self.healthbar.startposx = 2030
        self.bigenemy.health = 100

        self.healthbar.index = 0
        self.stabbing = False
        self.ammosprite.startposx = 2300
        self.exploding = False
        self.enemysprite.startposx = 1920
        self.enemysprite.startposy = self.enemysprite.gettypeenemy()
        self.enemysprite.speed = 10
        for h in self.healthbarlist:
            h.startposx = 2030
            h.index = 0
        self.highscorefunc()
        self.points = 0
        self.playersprite.ammunition = 30



    def collidecheck(self):
        self.playermask = pygame.mask.from_surface(self.displayedimage)
        self.enemymask = pygame.mask.from_surface(self.enemysprite.image)
        self.bigenemymask = pygame.mask.from_surface((self.bigenemy.image))
        offsetx = self.enemysprite.rect.left - self.displayedrect.left
        offsety = self.enemysprite.rect.top - self.displayedrect.top
        offsetx1 = self.bigenemy.rect.left - self.displayedrect.left
        offsety1 = self.bigenemy.rect.top - self.displayedrect.top
        if self.displayedrect.colliderect(self.enemysprite.rect) :
            if self.playermask.overlap(self.enemymask, (offsetx, offsety)):
                self.exploding = True
            elif self.enemysprite.rect.x > 1000:
                self.exploding = False
        elif self.displayedrect.colliderect(self.bigenemy.rect):
            if self.playermask.overlap(self.bigenemymask, (offsetx1,offsety1 )):
                self.stabbing = True
                self.healthbar.speed = 0.1
                self.bigenemy.stab()
                if self.bigenemy.rect.x < 250:
                    self.done = True
                    self.lost()
        elif self.enemysprite.rect.x < 0 and self.enemysprite.speed < 25:
            self.points += 1
            self.enemysprite.speed += self.points
        elif self.displayedrect.colliderect(self.ammosprite.rect):
            self.ammosprite.startposx = 2300
            ammcount = random.randint(10,30)
            self.playersprite.ammunition += ammcount
        for sprite in self.bulletgroup:
            if pygame.sprite.collide_mask(sprite,self.bigenemy) and self.bigenemy.imune is False:
                sprite.kill()
                self.bigenemy.health -= 10

    def shooting(self, dt):
        if self.playersprite.ammunition != 0:
            if self.playersprite.shooting and not self.playersprite.jumping and not self.playersprite.crouching:
                self.time_active += dt
                if self.time_active >= 100:
                    self.bulletgroup.add(self.playersprite.createbullet())
                    self.time_active = 0
                    self.playersprite.ammunition -= 1
        else:
            self.playersprite.shooting = False

    def highscorefunc(self):
        if self.points > self.highscore:
            self.highscore = self.points
            with open(path.join(self.dir, self.HS_FILE), 'w') as f:
                f.write(str(self.highscore))

    def get_kill(self):
        if self.bigenemy.health < 0:
            new_x_shift = random.randint(0,1000)
            self.points += 1
            self.bigenemysprites.pop()
            self.bigenemysprites.append(self.bigenemy)
            self.bigenemy.startposx = 2000 + new_x_shift
            self.healthbar.startposx = 2050 + new_x_shift
            self.bigenemy.health = 100
            self.healthbar.index = 0

    def explode(self):
        if self.exploding is True:
            speed = 3
            self.explosion.counter += 1
            if self.explosion.counter >= speed and self.explosion.index <= len(self.explosion.images):
                self.explosion.index += 1
                self.explosion.counter = 0
                if self.explosion.index != 4:
                    self.done = False
                else:
                    self.done = True
                    self.lost()
        else:
            self.explosion.index = 0


    def animation(self):
        if not self.playersprite.shooting and not self.playersprite.jumping and not self.playersprite.crouching:
            if self.playersprite.index >= len(self.playersprite.basicanimation):
                self.playersprite.index = 0
            self.displayedimage = self.playersprite.basicanimation[int(self.playersprite.index)]
            self.playersprite.index += .1
        elif self.playersprite.shooting and not self.playersprite.jumping:
            if self.playersprite.index >= len(self.playersprite.shootanimation):
                self.playersprite.index = 0
            self.displayedimage = self.playersprite.shootanimation[int(self.playersprite.index)]
            self.playersprite.index += .1
        elif self.playersprite.jumping:
            self.displayedimage = self.playersprite.imagejump
        elif self.playersprite.crouching:
            self.displayedimage = self.playersprite.slidingimage

    def hbanimation(self):
        try:
            for hb in self.healthbarlist:
                if self.bigenemy.health < 90:
                    hb.index = 1
                if self.bigenemy.health < 80:
                    hb.index = 2
                if self.bigenemy.health < 70:
                    hb.index = 3
                if self.bigenemy.health < 60:
                    hb.index = 4
                if self.bigenemy.health < 50:
                    hb.index = 5
                if self.bigenemy.health < 40:
                    hb.index = 6
                if self.bigenemy.health < 30:
                    hb.index = 7
                if self.bigenemy.health < 20:
                    hb.index = 8
                if self.bigenemy.health < 10:
                    hb.index = 9
        except:
            pass

    def update(self, dt):
        try:
            self.bigenemy.update()
        except:
            pass
        for hb in self.healthbarlist: hb.update()
        self.get_kill()
        self.hbanimation()
        self.playersprite.jump()
        self.animation()
        self.shooting(dt)
        self.bulletgroup.update()
        self.enemysprite.update()
        self.ammosprite.update()
        self.collidecheck()
        self.scoretext = f"SCORE: {self.points}"
        self.scoresurf = self.font.render(self.scoretext, True, "black")
        self.ammotext = f"AMMO:{self.playersprite.ammunition}"
        self.ammosurf = self.font.render(self.ammotext, True, "red")
        self.explode()
        self.explosion.update()

