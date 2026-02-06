import random
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
        self.state = "waiting"
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
        self.dydx = (0,0)
        self.start_location = (x, y)

        # Position and movement
        self.coords = (x, y)
        self.screen_coords = (x * config.TILE_SIZE, y * config.TILE_SIZE)
        self.target_coords = (x, y)
        self.target_screen_coords = (x * config.TILE_SIZE, y * config.TILE_SIZE)
        self.direction = "south"
        self.find_new_tile()

    def set_enclosure(self, enclosure):
        self.enclosure = enclosure

    def set_animal_state(self, state):
        self.state = state

    def set_animal_tile(self, tile):
        self.coords = tile
        self.screen_coords = (tile[0] * config.TILE_SIZE, tile[1] * config.TILE_SIZE)

    def draw(self):
        if self.direction == "left":
            self.screen.blit(self.image_left, self.screen_coords)
        else:
            self.screen.blit(self.image_right, self.screen_coords)

    def update(self, dt):
        if self.state == "moving":
            self.update_jump(dt)

        elif self.state == "idle":
            self.timer += dt
            if self.timer > self.activity_timer:
                self.timer = 0.0
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
            self.target_screen_coords = (x * config.TILE_SIZE, y * config.TILE_SIZE)
            print(f"x: {x}, y:{y}")
            self.calculate_coord_diff()

    def start_moving(self):
        """Initial calculation for jump"""
        self.state = "moving"
        self.jump_duration = random.randrange(1, 2)

        # Calculation of current jump distance (x)
        # Prevent over-movement
        if abs(self.dydx[1]) > 15:
            if self.dydx[1] > 0:
                jump = random.randrange(5, self.max_move_distance)
                self.direction = "right"
            else:
                jump = random.randrange(-1 * self.max_move_distance, -5)
                self.direction = "left"

            self.jump_x =  jump
        else:
            self.jump_x = self.dydx[1]

        # Calculation of current jump distance (y)
        if abs(self.dydx[0]) < 15:
            self.jump_y = self.dydx[0]

        else:

            self.jump_y = random.randrange(7, self.max_jump_height) if self.dydx[0] > 0 else (
                random.randrange(-1 * self.max_jump_height, -5)
            )

        print(f"jump: {self.jump_x}, jump_y: {self.jump_y}")
        self.start_location = self.screen_coords

    def update_jump(self, dt):
        self.timer += dt * 5

        # Check if jump is completed
        if self.timer > self.jump_duration:
            self.state = "idle"
            self.calculate_coord_diff()
            self.timer = 0.0
            self.activity_timer = random.randrange(0,150) / 100 # How many seconds to wait till next jump

            # If jump is near target, set to target
            x_threshold = self.dydx[0] < 7 and self.dydx[0] > 0
            y_threshold = self.dydx[1] < 7 and self.dydx[0] > 0
            if x_threshold and y_threshold:
                print("reached target")
                self.screen_coords = self.target_screen_coords
            self.coords = (self.screen_coords[0] // config.TILE_SIZE, self.screen_coords[1] // config.TILE_SIZE)
            return

        jump_progress = self.timer / self.jump_duration

        # X calculation during jump
        x = self.start_location[0] + self.jump_x * jump_progress

        # Jumping movement
        arc_height = math.sin(jump_progress * math.pi) * self.max_jump_height

        # Height gained after jump
        linear_climb = self.jump_y * jump_progress

        y = self.start_location[1] + linear_climb - arc_height

        self.screen_coords = (x, y)

    def calculate_coord_diff(self):
        """Calculates difference in x and y coordinates from target"""
        dy = self.target_screen_coords[1] - self.screen_coords[1]
        dx = self.target_screen_coords[0] - self.screen_coords[0]
        self.dydx = (dy, dx)
        print(f"dy: {dy}, dx: {dx}")