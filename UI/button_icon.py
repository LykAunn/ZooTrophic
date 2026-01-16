import pygame
from UI.button import Button

class ButtonIcon(Button):
    def __init__(self, image_path, image_path_clicked, y, x, callback = None):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image_pressed = pygame.image.load(image_path_clicked).convert_alpha()
        super().__init__(pygame.Rect(x ,y, self.image.get_width(), self.image.get_height()) ,callback=callback)
        
        self.current_image = self.image

        self.current_x = x
        self.current_y = y

        self.visible = False

    def handle_event(self, event):
        super().handle_event(event)
        self.current_image = self.image_pressed
        if self.pressed is True:
            self.current_image = self.image_pressed
        else:
            self.current_image = self.image

    def update_ypos(self, y):
        super().update_ypos(y)
        self.current_y = y
    
    def draw(self, screen):
        screen.blit(self.current_image, (self.current_x, self.current_y))