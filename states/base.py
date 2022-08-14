import pygame
from os import path


class BaseState(object):
    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.persist = {}
        self.font = pygame.font.Font("assets/Pixel.ttf", 24)
        self.HS_FILE = "highscore.txt"

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass

    def load_data(self):
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, self.HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        return self.highscore