import random
from importlib.metadata import pass_none
from unittest import case

import config
import pygame
import math

class Animal:
    def __init__(self, id, enclosure_id, x, y, species, image_path_left, image_path_right, screen, age = 0):
        # Identity
        self.animal_id = id
        self.age = age
        self.species = species
        self.sex = random.choice(["male", "female"])
        self.age_stage = "baby"
        self.name = None
        self.image_left = pygame.image.load(image_path_left).convert_alpha()
        self.image_left = pygame.transform.scale(self.image_left, (int(config.TILE_SIZE), int(config.TILE_SIZE)))
        self.image_right = pygame.image.load(image_path_right).convert_alpha()
        self.image_right = pygame.transform.scale(self.image_right, (int(config.TILE_SIZE), int(config.TILE_SIZE)))
        self.screen = screen

        # Enclosure
        self.enclosure_id = enclosure_id
        self.enclosure = None # Pointer to enclosure
        self.home_zone = None #TODO Specific tile of the enclosure to be animals home

        # Physical stats TODO
        self.health = 100.0
        self.max_health  = 100.0
        self.hunger = 50.0 # 0 - 100, higher = more hungry
        self.thirst = 50.0
        self.energy = 100.0
        self.size = 1.0

        #Psychological stats TODO
        self.happiness = 100
        self.stress = 0.0
        self.boredom = 0.0
        self.social_need = 50.0

        # Behaviour state TODO
        self.state = "HOVERING"
        self.activity_timer = 0.0 # Time to next activity (jump, find new tile)
        self.last_fed = 0
        self.last_drank = 0
        self.last_slept = 0

        # Movement
        self.timer = 0.0
        self.jump_duration = 0.0
        self.max_jump_height = 15
        self.max_move_distance = 25
        self.jump_x = 0                   # Pixels to move in that jump
        self.jump_y = 0
        self.pixel_delta = (0, 0) # (dy, dx)
        self.jump_start_pos = (x, y)

        # Position and movement
        self.coords = (x, y)
        self.world_pixel_coords = (x * config.TILE_SIZE, y * config.TILE_SIZE)
        self.target_coords = (x, y)
        self.target_world_pixel_coords = (x * config.TILE_SIZE, y * config.TILE_SIZE)
        self.direction = "south"

        # Data
        self.hunger_rate = 0.8
        self.thirst_rate = 1
        self.social_type = None
        self.min_enclosure_size = 10
        self.energy_drain = 0.1
        self.max_number_of_animals = 2
        self.stat_update_timer = 3 # Stat update interval
        self.stat_timer = 0.0

    def set_enclosure(self, enclosure):
        self.enclosure = enclosure

    def set_animal_state(self, state):
        self.state = state

    def set_animal_tile(self, tile):
        """Sets animals coordinates to input tile (x,y)"""
        self.coords = tile
        self.world_pixel_coords = (tile[0] * config.TILE_SIZE, tile[1] * config.TILE_SIZE)

    def draw(self, camera_offset):
        offsetScreenX = self.world_pixel_coords[0]
        offsetScreenY = self.world_pixel_coords[1]

        if self.state != "HOVERING":
            offsetScreenX -= camera_offset[0] * config.TILE_SIZE
            offsetScreenY -= camera_offset[1] * config.TILE_SIZE

        if self.direction == "left":
            self.screen.blit(self.image_left, (offsetScreenX, offsetScreenY))
        else:
            self.screen.blit(self.image_right, (offsetScreenX, offsetScreenY))

    def update(self, dt, mousepos):
        # Update stats of animal
        self.update_needs(dt)
        self.stat_timer += dt
        if self.stat_timer > self.stat_update_timer:
            self.update_animal()
            self.stat_timer = 0.0

        if self.state == "MOVING":
            self.update_jump(dt)

        elif self.state == "IDLE":
            self.timer += dt
            if self.timer > self.activity_timer:
                self.timer = 0.0
                self.decide_next_action()
            
        elif self.state == "HOVERING":
            padding = config.TILE_SIZE // 2
            self.world_pixel_coords = (mousepos[0] - padding, mousepos[1] - padding)

    def decide_next_action(self):
        """Choose what to do next, prioritises hunger and thirst. If not then wander around"""
        #if self.thirst > 70:
            #self.find_water_source()
        if self.hunger > 70: #TODO: keeps finding food source when deciding next action, should start moving instead
            self.find_food_source()
        else:
            if self.target_coords == self.coords:
                self.find_new_tile()
            else:
                self.start_moving()

# --- Pathfinding ---

    def find_new_tile(self):
        """Finds new tile to wander to"""
        if self.enclosure:
            x, y = random.choice(list(self.enclosure.interior_tiles))
            self.target_coords = (x, y)
            self.target_world_pixel_coords = (x * config.TILE_SIZE, y * config.TILE_SIZE)
            print(f"x: {x}, y:{y}")
            self.calculate_coord_diff()

    def start_moving(self):
        """Initial calculation for jump"""
        self.state = "MOVING"
        self.jump_duration = random.randrange(1, 2)

        # Calculation of current jump distance (x)
        # Prevent over-movement
        if abs(self.pixel_delta[1]) > 15:
            if self.pixel_delta[1] > 0:
                jump = random.randrange(5, self.max_move_distance)
                self.direction = "right"
            else:
                jump = random.randrange(-1 * self.max_move_distance, -5)
                self.direction = "left"

            self.jump_x =  jump
        else:
            self.jump_x = self.pixel_delta[1]

        # Calculation of current jump distance (y)
        if abs(self.pixel_delta[0]) < 15:
            self.jump_y = self.pixel_delta[0]

        else:

            self.jump_y = random.randrange(7, self.max_jump_height) if self.pixel_delta[0] > 0 else (
                random.randrange(-1 * self.max_jump_height, -5)
            )

        #print(f"jump: {self.jump_x}, jump_y: {self.jump_y}")
        self.jump_start_pos = self.world_pixel_coords

    def update_jump(self, dt):
        self.timer += dt * 5

        # Check if jump is completed
        if self.timer > self.jump_duration:
            self.state = "IDLE"
            self.calculate_coord_diff()
            self.timer = 0.0
            self.activity_timer = random.randrange(0,150) / 100 # How many seconds to wait till next jump
            self.energy -= self.energy_drain

            # Snap to target if close enough
            if abs(self.pixel_delta[0]) < 7 and abs(self.pixel_delta[1]) < 7:
                print("reached target")
                self.world_pixel_coords = self.target_world_pixel_coords
                # print(self.happiness)
            self.coords = (self.world_pixel_coords[0] // config.TILE_SIZE, self.world_pixel_coords[1] // config.TILE_SIZE)
            return

        jump_progress = self.timer / self.jump_duration

        # X calculation during jump
        x = self.jump_start_pos[0] + self.jump_x * jump_progress

        # Jumping movement
        arc_height = math.sin(jump_progress * math.pi) * self.max_jump_height

        # Height gained after jump
        linear_climb = self.jump_y * jump_progress

        y = self.jump_start_pos[1] + linear_climb - arc_height

        self.world_pixel_coords = (int(x), int(y))

    def calculate_coord_diff(self):
        """Calculates difference in x and y coordinates from target"""
        dy = self.target_world_pixel_coords[1] - self.world_pixel_coords[1]
        dx = self.target_world_pixel_coords[0] - self.world_pixel_coords[0]
        self.pixel_delta = (dy, dx)
        #print(f"dy: {dy}, dx: {dx}")

    def update_needs(self, scaled_dt):
        self.hunger += scaled_dt * self.hunger_rate if self.hunger < 100 else 0
        self.thirst += scaled_dt * self.thirst_rate if self.thirst < 100 else 0

    def calculate_stress(self):
        self.stress = 0
        # print("Animal enclosure size = ", self.enclosure.enclosure_size)
        if self.enclosure.enclosure_size < self.min_enclosure_size:
            self.stress += 20
        if self.enclosure.animals_in_enclosure > self.max_number_of_animals:
            self.stress += 20

    def animals_nearby(self):
        return self.enclosure.animals_in_enclosure #TODO Calculate number of animals nearby in the enclosure

    def calculate_animal_social_bonus(self):
        animals_nearby = self.animals_nearby()
        match self.social_type:
            case 0:
                if animals_nearby == 0:
                    return 10
                return 0
            case 1:
                if animals_nearby == 1:
                    return 10
                return 0
            case 2:
                if animals_nearby > 2:
                    return 10
                return 0
        return 0

    def calculate_happiness(self):
        hunger_penalty = max(0, (self.hunger - 50) / 50)
        thirst_penalty = max(0, (self.thirst - 40) / 60)
        self.calculate_stress()
        stress_penalty = self.stress / 100
        social_bonus = self.calculate_animal_social_bonus()

        self.happiness = 100 - (hunger_penalty + thirst_penalty + stress_penalty) * 33 + social_bonus * 10

    def update_animal(self):
        """Updates stress and happiness of animal"""
        self.calculate_stress()
        self.calculate_happiness()
        #print(self.hunger)

    def find_food_source(self):
        food_tile = self.enclosure.get_nearest_food_tile(self.coords)
        if food_tile:
            self.target_coords = food_tile.position
            self.target_world_pixel_coords = (food_tile.position[0] * config.TILE_SIZE,
                                              food_tile.position[1] * config.TILE_SIZE)
            self.calculate_coord_diff()
            if self.pixel_delta[0] > 0 and self.pixel_delta[1] > 0:
                self.start_moving()
        else:
            return

    def find_water_source(self):
        pass

    def get_hunger(self):
        return int(self.hunger), 100

    def get_thirst(self):
        return self.thirst, 100

    def get_happiness(self):
        return int(self.happiness), 100