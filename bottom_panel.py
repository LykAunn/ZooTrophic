import pygame
import config
from menu import Menu
from button import Button

class BottomPanel(Menu):
    def __init__(self, screen):
        super().__init__(screen, config.SCREENHEIGHT, False, 150, config.SCREENHEIGHT)

        self.selected_enclosure = None
        self.buttons = []
        self.button = Button(pygame.Rect(20, self.current_y + 50, 100, 20), "BUILD")

    def show(self, enclosure):
        self.selected_enclosure = enclosure
        self.target_y = config.SCREENHEIGHT - self.menu_height
        self.is_visible = True

    def draw(self):
        if self.current_y >= config.SCREENHEIGHT:
            return
        
        menu_rect = pygame.Rect(0, int(self.current_y), config.SCREENWIDTH, self.menu_height)

        pygame.draw.rect(self.screen, "darkgoldenrod4", menu_rect)
        pygame.draw.rect(self.screen, "black", menu_rect, 2)

        self.button.draw(self.screen)

    def update(self, dt):
        super().update(dt)
        self.button.update_ypos(self.current_y + 50)

    def handle_event(self, event):
        self.button.handle_event(event)