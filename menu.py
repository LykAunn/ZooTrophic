import pygame
import config

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.is_visible = False
        self.current_y = config.SCREENHEIGHT
        self.target_y = config.SCREENHEIGHT
        self.menu_height = 150
        self.slide_speed = config.menu_movement_speed

        self.selected_enclosure = None
        self.buttons = []

    def show(self, enclosure):
        self.selected_enclosure = enclosure
        self.target_y = config.SCREENHEIGHT - self.menu_height
        self.is_visible = True
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!SHOW")
        print(self.target_y)

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
        print("DRAW MENU")

    def hide(self):
        self.selected_enclosure = None
        self.target_y = config.SCREENHEIGHT