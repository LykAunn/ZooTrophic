import pygame
import config
from menu import Menu

class BottomPanel(Menu):
    def __init__(self, screen):
        super().__init__(screen, config.SCREENHEIGHT, False, 150, config.SCREENHEIGHT)

        self.selected_enclosure = None
        self.buttons = []

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
        print("DRAW MENU")