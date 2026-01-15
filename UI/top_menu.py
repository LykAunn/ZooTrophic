import config
import pygame

class TopPanel:
    def __init__(self, screen):
        self.screen = screen
        self.is_visible = True
        self.current_y = -50
        self.target_y = -50
        self.menu_height = 30
        self.slide_speed = config.menu_movement_speed

        self.buttons = []

    def show(self):
        self.target_y = 0
        self.is_visible = True

    def update(self,dt):
        if abs(self.current_y - self.target_y) > 0.5:
            diff = self.target_y - self.current_y
            self.current_y += diff * self.slide_speed * dt
        
        else:
            self.current_y = self.target_y

    def draw(self):
        if self.current_y <= -50:
            return
        
        menu_rect = pygame.Rect(0, int(self.current_y), config.SCREENWIDTH, self.menu_height)

        pygame.draw.rect(self.screen, 0x9D7750, menu_rect)
        # pygame.draw.rect(self.screen, "black", menu_rect, 2)

    def hide(self):
        self.selected_enclosure = None
        self.target_y = -50