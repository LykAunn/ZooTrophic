import config
import pygame

class Cursor:
    def __init__(self, screen, image_path):
        self.screen = screen
        self.tilesize = config.TILE_SIZE
        self.max_tile = config.noOfTiles_x
        self.screen_x = 0
        self.screen_y = 0
        self.cursor_image = pygame.image.load(image_path).convert_alpha()
        self.cursor_image = pygame.transform.scale(self.cursor_image, (int(config.TILE_SIZE), int(config.TILE_SIZE)))
        self.visible = True

    def update(self, mouse_pos, camera_offset):
        offset_x = (camera_offset[0] % 1) * self.tilesize
        offset_y = (camera_offset[1] % 1) * self.tilesize

        self.screen_x = ((mouse_pos[0] + offset_x) // self.tilesize) * self.tilesize - offset_x
        self.screen_y = ((mouse_pos[1] + offset_y) // self.tilesize) * self.tilesize - offset_y

    def draw_cursor(self):
        if self.screen_x < 0 or self.screen_x >= config.SCREENWIDTH:
            return
        if self.screen_y < 0 or self.screen_y >= config.SCREENHEIGHT:
            return

        self.screen.blit(self.cursor_image, (self.screen_x, self.screen_y))