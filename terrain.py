import config
import pygame

class TerrainRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.grass_variants =  [pygame.image.load("resources/grass.png").convert_alpha(), pygame.image.load("resources/grass2.png").convert_alpha(),
                                pygame.image.load("resources/grass4.png").convert_alpha()]

    def get_grass_variant(self, tile_x, tile_y):
        seed = (tile_x * 73856093) ^ (tile_y * 19349663)
        index = seed % len(self.grass_variants)
        return self.grass_variants[index]

    def draw(self, camera_offset, end_x, end_y, ):
        for tile_x in range(int(camera_offset[0] - 1), int(end_x) + 1):
            for tile_y in range(int(camera_offset[1] - 1), int(end_y) + 1):
                screen_x = (tile_x - camera_offset[0]) * config.TILE_SIZE
                screen_y = (tile_y - camera_offset[1]) * config.TILE_SIZE

                grass = self.get_grass_variant(tile_x, tile_y)
                self.screen.blit(grass, (screen_x, screen_y))