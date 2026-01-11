import config
import pygame
from button import Button

class Menu:
    """Base class for all Menu objects"""
    def __init__(self, screen, y, visible, height, default_position, game_manager):
        self.screen = screen
        self.is_visible = visible
        self.current_y = y
        self.target_y = y
        self.menu_height = height
        self.slide_speed = config.menu_movement_speed
        self.default_position = default_position
        self.game_manager = game_manager

    def show(self):
        self.target_y = self.default_position - self.menu_height
        self.is_visible = True

    def update(self,dt):
        if abs(self.current_y - self.target_y) > 0.5:
            diff = self.target_y - self.current_y
            self.current_y += diff * self.slide_speed * dt
        
        else:
            self.current_y = self.target_y

    def draw(self):
        if self.current_y >= config.SCREENHEIGHT:
            return
        
        menu_rect = pygame.Rect(0, int(self.current_y), config.SCREENWIDTH, self.menu_height)

        pygame.draw.rect(self.screen, "darkgoldenrod4", menu_rect)
        pygame.draw.rect(self.screen, "black", menu_rect, 2)

    def hide(self):
        self.selected_enclosure = None
        self.target_y = config.SCREENHEIGHT