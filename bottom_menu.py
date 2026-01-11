from menu import Menu
import config
from button import Button
import pygame

class BottomMenu(Menu):
    def __init__(self, screen, height, game_manager):
        super().__init__(screen, config.SCREENHEIGHT, True, height, config.SCREENHEIGHT, game_manager)

        self.buttons = []
        self.button = Button(pygame.Rect(20, self.current_y + 20, 100, 20), "BUILD", game_manager.on_build_clicked)

    def update(self, dt):
        super().update(dt)
        self.button.update_ypos(self.current_y + 20)

    def handle_event(self, event):
        if self.is_visible:
            self.button.handle_event(event)

    def draw(self):
        super().draw()
        self.button.draw(self.screen)