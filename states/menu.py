import pygame
from .base import BaseState
from spritesheet import Spritesheet

class Menu(BaseState):
    def __init__(self):
        super(Menu, self).__init__()
        self.active_index = 0
        self.options = ["Start Game", "Quit Game"]
        myspritesheet = Spritesheet("assets/logo.png")
        self.title = myspritesheet.parse_sprite("New Piskel0.png")
        self.title = pygame.transform.scale(self.title,(1920,1080))
        self.next_state = "GAMEPLAY"
        self.load_data()
        self.hstext = f"YOUR HIGHSCORE IS: {self.highscore}"
        self.hssurf = self.font.render(self.hstext,True,"red")

    def render_text(self, index):
        color = pygame.Color("red") if index == self.active_index else pygame.Color("white")
        return self.font.render(self.options[index], True, color)

    def get_text_position(self, text, index):
        center = (self.screen_rect.center[0], self.screen_rect.center[1] + (index * 50))
        return text.get_rect(center=center)

    def handle_action(self):
        if self.active_index == 0:
            self.done = True
        elif self.active_index == 1:
            self.quit = True

    def update(self,dt):
        self.load_data()
        self.hstext = f"YOUR HIGHSCORE IS: {self.highscore}"
        self.hssurf = self.font.render(self.hstext, True, "red")

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.active_index = 1 if self.active_index <= 0 else 0
            elif event.key == pygame.K_DOWN:
                self.active_index = 0 if self.active_index >= 1 else 1
            elif event.key == pygame.K_RETURN:
                self.handle_action()

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.hssurf,(1920/2-179,1080/2-100))
        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            surface.blit(text_render, self.get_text_position(text_render, index))
            surface.blit(self.title,(425,1080/2-350))