import pygame
import config
from UI.menu import Menu
from UI.button import Button

class BottomPanel(Menu):
    def __init__(self, screen, game_manager):
        super().__init__(screen, config.SCREENHEIGHT, False, 80, config.SCREENHEIGHT, game_manager)

        self.selected_enclosure = None
        self.buttons = []
        self.button = Button(pygame.Rect(300, self.current_y + 25, 100, 20), "BUILD")
        self.menu_image = pygame.image.load("resources/Bottom_Menu.png").convert_alpha()
        self.menu_image = pygame.transform.scale_by(self.menu_image, config.pixel_size)

    def show(self, enclosure):
        self.selected_enclosure = enclosure
        self.target_y = config.SCREENHEIGHT - self.menu_height
        self.is_visible = True

    def draw(self):
        if self.current_y >= config.SCREENHEIGHT:
            return
        
        x = (config.SCREENWIDTH / 2) - (self.menu_image.get_width() / 2)
        self.screen.blit(self.menu_image, (x, self.current_y))

        self.button.draw(self.screen)

    def update(self, dt):
        super().update(dt)
        self.button.update_ypos(self.current_y + 25)

    def handle_event(self, event):
        self.button.handle_event(event)