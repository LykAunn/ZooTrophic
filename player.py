import config
import pygame

class Player:
    def __init__(self):
        self.world_x = 20
        self.world_y = 11
        self.speed = config.fill_speed

    def update(self, dt):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.world_y -= self.speed * dt
        
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.world_y += self.speed * dt
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.world_x -= self.speed * dt
        
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.world_x += self.speed * dt

    # def handle_event(self, event):
    #     # one-time actions like jumping, interacting, etc.
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_SPACE:
    #             self.interact()
    #         elif event.key == pygame.K_e:
    #             self.open_inventory()
    
    def get_position(self):
        return self.world_x, self.world_y