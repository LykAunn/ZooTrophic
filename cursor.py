import config
import pygame

class Cursor:
    def __init__(self, screen, image_path):
        self.screen = screen
        self.tilesize = config.TILE_SIZE
        self.max_tile = config.noOfTiles
        self.x_coord = 0
        self.y_coord = 0
        self.cursor_image = pygame.image.load(image_path).convert_alpha()
        self.cursor_image = pygame.transform.scale(self.cursor_image, (int(config.TILE_SIZE), int(config.TILE_SIZE)))
        self.visible = True

    def update(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord

    def draw_cursor(self):
        if self.x_coord > self.max_tile or self.y_coord > self.max_tile:
            return

        self.screen.blit(self.cursor_image, (self.x_coord * self.tilesize, self.y_coord * self.tilesize))