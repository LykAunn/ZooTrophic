import pygame

class textBox:
    def __init__(self, screen, x, y, width, height):
        self.screen = screen
        self.coords = (x,y)
        self.image = pygame.image.load('resources/text_box.png').convert_alpha()
        self.text = ''

    def update_text(self, text):
        self.text = text

    def draw(self):
        self.screen.blit(self.image, self.coords)