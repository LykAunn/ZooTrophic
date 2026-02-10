import pygame
import pygame.gfxdraw
import config

class ClockMenu:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.clock_image = pygame.image.load('resources/daynightcycle.png').convert()
        self.clock_image = pygame.transform.scale(self.clock_image, (int(config.TILE_SIZE) * 2, int(config.TILE_SIZE) * 2))
        self.arrow_image = None

        # Clock
        self.current_rotation = 0
        self.target_rotation = 0
        self.clock_counter = 0
        self.clock_location = (50, 50)
        self.mask_size = int(config.TILE_SIZE) * 2
        self.mask = pygame.Surface((self.mask_size, self.mask_size), pygame.SRCALPHA)
        pygame.draw.circle(self.mask, (255, 255, 255, 255), (self.mask_size //2, self.mask_size // 2), self.mask_size // 2)

    def draw(self, screen):
        pygame.gfxdraw.aacircle(screen, 500, 500, 50, (0,0,0))
        pygame.gfxdraw.filled_circle(screen, 500,500,50,(0,0,0))
        rotated_clock = pygame.transform.rotate(self.clock_image, self.current_rotation)

        temp_surface = pygame.Surface((self.mask_size, self.mask_size), pygame.SRCALPHA)
        rotated_rect = rotated_clock.get_rect(center=(self.mask_size // 2, self.mask_size // 2))
        temp_surface.blit(rotated_clock, rotated_rect)

        temp_surface.blit(self.mask, (0,0), special_flags=pygame.BLEND_RGBA_MIN)

        screen.blit(temp_surface, self.clock_location)

    def update(self, dt):
        self.clock_counter += dt
        if self.clock_counter >= 0.1 and abs(self.target_rotation - self.current_rotation) > 0:
            self.current_rotation += 1
            self.clock_counter = 0
            print("ADDING")

    def increment_hour(self):
        self.target_rotation += 15
        if self.target_rotation >= 360:
            self.target_rotation = 0

    def set_rotation(self, rotation):
        self.target_rotation = rotation