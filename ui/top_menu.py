import config
import pygame

class TopPanel:
    def __init__(self, screen):
        self.screen = screen
        self.is_visible = True
        self.menu_image = pygame.image.load("resources/top_menu.png").convert_alpha()
        self.menu_image = pygame.transform.scale(self.menu_image, ((config.noOfTiles_x - 5) * config.TILE_SIZE, config.TILE_SIZE * 2))
        self.current_y = -50
        self.target_y = -50
        self.x = config.SCREENWIDTH - self.menu_image.get_width() - (config.TILE_SIZE // 2.5)
        self.menu_height = 30
        self.slide_speed = config.menu_movement_speed

        self.buttons = []

    def show(self):
        self.target_y = 0
        self.is_visible = True

    def update(self,dt):
        if abs(self.current_y - self.target_y) > 0.5:
            diff = self.target_y - self.current_y
            self.current_y += diff * self.slide_speed * dt
        
        else:
            self.current_y = self.target_y

    def draw(self):
        if self.current_y <= -50:
            return
        
        # menu_rect = pygame.Rect(0, int(self.current_y), config.SCREENWIDTH, self.menu_height)
        self.screen.blit(self.menu_image, (self.x, self.current_y))

        #pygame.draw.rect(self.screen, 0x9D7750, menu_rect)
        # pygame.draw.rect(self.screen, "black", menu_rect, 2)

    def hide(self):
        self.selected_enclosure = None
        self.target_y = -50