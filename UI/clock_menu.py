import pygame
import pygame.gfxdraw
import config

class ClockMenu:
    def __init__(self, x, y, radius, game_clock):
        self.x = x
        self.y = y
        self.radius = radius
        self.clock_image = pygame.image.load('resources/day_night_dial.png').convert_alpha()
        self.clock_image = pygame.transform.scale(self.clock_image, (int(config.TILE_SIZE) * 2.5, int(config.TILE_SIZE) * 2.5))
        self.hanging_sign_image = pygame.image.load('resources/Hanging_Sign.png').convert_alpha()
        self.hanging_sign_image = pygame.transform.scale(self.hanging_sign_image, (int(config.TILE_SIZE) * 3, int(config.TILE_SIZE) * 3))
        self.hanging_sign_location = (0,0)
        self.arrow_image = None
        self.game_clock = game_clock

        # Clock
        self.current_rotation = 0
        self.target_rotation = 0
        self.clock_counter = 0
        self.clock_location = (54,12)
        self.mask_size = int(config.TILE_SIZE) * 2.5
        self.mask = pygame.Surface((self.mask_size, self.mask_size), pygame.SRCALPHA) #SRCALPHA = Transparent
        pygame.draw.circle(self.mask, (255, 255, 255, 255), (self.mask_size // 2, self.mask_size // 2), self.mask_size // 2)
        # Draw white circle on transparent background

        # Font
        self.time_text = "None"
        self.date_text = "None"
        try: # Try to load font
            self.font = pygame.font.Font('resources/font.ttf', 24)
        except FileNotFoundError:
            print("Font not found, using default.")
            self.font = pygame.font.Font(None, 24)

        self.time_surf = self.font.render("None", True, (0, 0, 0))
        self.date_surf = self.font.render("None", True, (0, 0, 0))

    def draw(self, screen):
        pygame.gfxdraw.aacircle(screen, 500, 500, 50, (0,0,0))
        pygame.gfxdraw.filled_circle(screen, 500,500,50,(0,0,0))
        rotated_clock = pygame.transform.rotate(self.clock_image, self.current_rotation)

        temp_surface = pygame.Surface((self.mask_size, self.mask_size), pygame.SRCALPHA)
        rotated_rect = rotated_clock.get_rect(center=(self.mask_size // 2, self.mask_size // 2))
        temp_surface.blit(rotated_clock, rotated_rect) # Blit clock onto top left position of rotated rect

        # Only inner white circle will be shown
        temp_surface.blit(self.mask, (0,0), special_flags=pygame.BLEND_RGBA_MIN)

        screen.blit(temp_surface, self.clock_location)
        screen.blit(self.hanging_sign_image, self.hanging_sign_location)

        # Time display
        screen.blit(self.time_surf, (self.x - 30, self.y))

        # Date display
        screen.blit(self.date_surf, (self.x - 30, self.y + 100))

    def update(self, dt):
        self.clock_counter += dt
        if self.clock_counter >= 0.1 and abs(self.target_rotation - self.current_rotation) > 0:
            self.current_rotation += 1
            self.clock_counter = 0
        
        if self.current_rotation >= 360:
            self.current_rotation = 0

        # Update time display
        self.time_text= self.game_clock.get_formatted_time()
        self.time_surf = self.font.render(self.time_text, True, (0, 0, 0))

        # Update Date display
        self.date_text = self.game_clock.get_formatted_date()
        self.date_surf = self.font.render(self.date_text, True, (0, 0, 0))

    def increment_hour(self):
        self.target_rotation += 15
        if self.target_rotation >= 360:
            self.target_rotation = 0

        # print(f"target: {self.target_rotation}")
        # print(f"current: {self.current_rotation}")

    def set_rotation(self, rotation):
        self.target_rotation = rotation