import math

import pygame

import config

class ClockMenu:
    def __init__(self, x, y, radius, game_clock):
        self.menu_scale = 4
        self.radius = radius
        self.clock_image = pygame.image.load('resources/day_night_dial.png').convert_alpha()
        self.clock_image = pygame.transform.scale(self.clock_image, (int(config.TILE_SIZE) * 2.5, int(config.TILE_SIZE) * 2.5))
        self.hanging_sign_image = pygame.image.load('resources/Hanging_Sign.png').convert_alpha()
        self.hanging_sign_image = pygame.transform.scale(self.hanging_sign_image, (int(config.TILE_SIZE) * self.menu_scale, int(config.TILE_SIZE) * self.menu_scale))
        self.hanging_sign_location = (config.TILE_SIZE // 4,0) #(x, y)
        self.game_clock = game_clock
        self.visible = True

        # Clock
        self.current_rotation = 0
        self.target_rotation = 0
        self.clock_counter = 0
        self.mask_size = int(config.TILE_SIZE) * 2.5
        self.clock_location = (self.hanging_sign_location[0] + (config.pixel_size * 48) - self.mask_size // 2,
                               self.hanging_sign_location[1] + config.pixel_size * 28 - self.mask_size // 2)
        self.mask = pygame.Surface((self.mask_size, self.mask_size), pygame.SRCALPHA) #SRCALPHA = Transparent
        # Draw white circle on transparent background
        pygame.draw.circle(self.mask,
                           (255, 255, 255, 255),
                           (self.mask_size // 2,
                            self.mask_size // 2),
                           self.mask_size // 2)

        # Glow
        self.glow_intensity = 0.0

        # Clicking
        self.hovered = False
        self.clock_center = (self.clock_location[0] + self.mask_size // 2, self.clock_location[1] + self.mask_size // 2)
        self.click_radius = self.mask_size // 2

        # Font
        self.time_text = "None"
        self.date_text = "None"
        try: # Try to load font
            self.font = pygame.font.Font('resources/font.ttf', 20)
        except FileNotFoundError:
            print("Font not found, using default.")
            self.font = pygame.font.Font(None, 20)

        # Text
        self.time_surf = self.font.render("None", True, (0, 0, 0))
        self.time_location = (self.hanging_sign_location[0] + (config.pixel_size * 8),
                              self.hanging_sign_location[1] + (config.pixel_size * 10))
        self.date_surf = self.font.render("None", True, (0, 0, 0))
        self.date_location = ()

    def draw(self, screen):
        # pygame.gfxdraw.aacircle(screen, 500, 500, 50, (0,0,0))
        # pygame.gfxdraw.filled_circle(screen, 500,500,50,(0,0,0))
        rotated_clock = pygame.transform.rotate(self.clock_image, self.current_rotation)

        temp_surface = pygame.Surface((self.mask_size, self.mask_size), pygame.SRCALPHA)
        rotated_rect = rotated_clock.get_rect(center=(self.mask_size // 2, self.mask_size // 2))
        temp_surface.blit(rotated_clock, rotated_rect) # Blit clock onto top left position of rotated rect

        # Only inner white circle will be shown
        temp_surface.blit(self.mask, (0,0), special_flags=pygame.BLEND_RGBA_MIN)

        screen.blit(temp_surface, self.clock_location)

        # Glow surface
        if self.glow_intensity > 0.01:
            glow_surface = pygame.Surface((self.click_radius * 2, self.click_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                glow_surface,
                (181, 89, 69, int(self.glow_intensity * 128)),
                (self.click_radius, self.click_radius),
                self.click_radius
            )
            screen.blit(glow_surface,
                        (self.clock_center[0] - self.click_radius, self.clock_center[1] - self.click_radius))

        # Hanging sign
        screen.blit(self.hanging_sign_image, self.hanging_sign_location)

        # Time display
        screen.blit(self.time_surf, self.time_location)

        # Date display
        screen.blit(self.date_surf, self.hanging_sign_location)

    def update_glow(self, is_glow, dt):
        target_glow = 1.0 if is_glow else 0.0

        glow_speed = 7
        difference = target_glow - self.glow_intensity
        self.glow_intensity += difference * glow_speed * dt

        self.glow_intensity = max(0.0, min(1.0, self.glow_intensity))

    def update(self, dt):
        self.clock_counter += dt
        if self.clock_counter >= 0.1 and abs(self.target_rotation - self.current_rotation) > 0:
            self.current_rotation += 1
            self.clock_counter = 0

        self.update_glow(self.game_clock.paused, dt)
        
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

    def set_rotation(self, rotation):
        self.target_rotation = rotation

    def is_point_in_clock(self, pos):
        dx = pos[0] - self.clock_center[0]
        dy = pos[1] - self.clock_center[1]
        distance = math.sqrt(dx * dx + dy * dy)
        return distance <= self.click_radius and pos[0] >= self.clock_center[0]

    def handle_event(self, event):
        if self.visible:
                if event.type == pygame.MOUSEMOTION:
                    self.hovered = self.is_point_in_clock(event.pos)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.is_point_in_clock(event.pos):
                        self.on_clock_clicked()

    def on_clock_clicked(self):
        self.game_clock.toggle_pause()