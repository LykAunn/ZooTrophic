import random
import config
import pygame
import math

class Animal:
    def __init__(self, id, enclosure_id, x, y, species, image_path, screen, age = 0):
        # Identity
        self.animal_id = id
        self.age = age
        self.species = species
        self.sex = random.choice(["male", "female"])
        self.age_stage = "baby"
        self.name = None
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(config.TILE_SIZE), int(config.TILE_SIZE)))
        self.screen = screen

        # Enclosure
        self.enclosure_id = enclosure_id
        self.enclosure = None # Reference for enclosure
        self.home_zone = None

        # Physical stats
        self.health = 100.0
        self.max_health  = 100.0
        self.hunger = 50.0 # 0 - 100, higher = more hungry
        self.thirst = 50.0
        self.energy = 100.0
        self.size = 1.0

        #Psychological stats
        self.happiness = 100
        self.stress = 0.0
        self.boredom = 0.0
        self.social_need = 50.0

        # Behaviour state  
        self.state = "idle"
        self.activity_timer = 0.0
        self.last_fed = 0
        self.last_drank = 0
        self.last_slept = 0

        # Movement
        self.time_till_next_move = 0.0
        self.jump_timer = 0.0
        self.jump_duration = 0.0
        self.max_jump_height = 15
        self.max_move_distance = 15
        self.jumpx = 0                   # Pixels to move in that current jump
        self.jumpy = 0
        self.dxdy = (0,0)
        self.start_location = (x, y)

        # Position and movement
        self.coords = (x, y)
        self.screen_coords = (x * config.TILE_SIZE, y * config.TILE_SIZE)
        self.target_coords = (x, y)
        self.target_screen_coords = (x * config.TILE_SIZE, y * config.TILE_SIZE)
        self.speed = 2.0
        self.direction = "south"

    def set_enclosure(self, enclosure):
        self.enclosure = enclosure

    def draw(self):
        self.screen.blit(self.image, self.screen_coords)

    def update(self, dt):
        if self.state == "moving":
            self.update_jump(dt)


# --- Pathfinding ---

    def find_new_tile(self):
        x, y = random.choice(self.enclosure.interior_tiles)
        self.target_coords = (x, y)
        self.target_screen_coords = (x * config.TILE_SIZE, y * config.TILE_SIZE)

    def start_moving(self):
        self.state = "moving"
        self.jump_duration = random.randrange(1, 2)
        self.jump_progress = 0.0
        # self.dxdy = self.target_screen_coords - self.screen_coords
        # if self.dxdy[0] < self.max_move_distance and self.dxdy[1] < self.max_jump_height:
        #     self.jumpx = self.dxdy[0]
        #     self.jumpy = self.dxdy[1]
        # else:
        #     self.jumpx = random.randrange(5, self.max_move_distance)
        #     self.jumpy = random.randrange(5, self.max_jump_height)
        self.jumpx = 100
        self.jumpy = 100
        self.start_location = self.screen_coords

    def update_jump(self, dt):
        self.jump_timer += dt

        if self.jump_timer > self.jump_duration:
            self.state = "idle"
            # self.screen_coords = self.target_screen_coords
            self.coords = self.target_coords
            self.jump_timer = 0.0

        jump_progress = self.jump_timer / self.jump_duration

        x = self.start_location[0] + self.jumpx * jump_progress

        arc_height = math.sin(jump_progress * math.pi) * abs(self.jumpy)

        linear_climb = abs(self.jumpy) * jump_progress

        y_change = -1 if self.jumpy < 0 else 1

        y = self.start_location[1] + (linear_climb * y_change) - arc_height

        self.screen_coords = (x, y)