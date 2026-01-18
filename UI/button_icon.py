import pygame
import config
from UI.button import Button

class ButtonIcon(Button):
    def __init__(self, image_path, image_path_clicked, y, x, callback = None):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image_pressed = pygame.image.load(image_path_clicked).convert_alpha()
        super().__init__(pygame.Rect(x ,y, self.image.get_width(), self.image.get_height()) ,callback=callback)
        
        self.current_image = self.image

        self.current_x = x

        self.visible = True

    def handle_event(self, event):
        super().handle_event(event)
        self.current_image = self.image_pressed
        if self.pressed is True:
            self.current_image = self.image_pressed
        else:
            self.current_image = self.image
    
    def draw(self, screen):
        if self.current_y >= config.SCREENHEIGHT:
            return
        
        screen.blit(self.current_image, (self.current_x, self.current_y))