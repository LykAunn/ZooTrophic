from objects.food_dish import FoodDish
from world.tile_index import TileIndex
import pygame
import config

class ObjectManager:
    def __init__(self, tile_index, screen):
        self.tile_index = tile_index
        self.screen = screen
        self.objects = {} # Dictionary storing object id as a key and object reference as value
        self.next_id = 0
        self.state = "NONE"
        self.pending_object = None
        self.pending_pos = (0,0)

        # Tile sprite
        self.food = pygame.image.load('resources/food.png').convert_alpha()
        self.food = pygame.transform.scale(self.food, (int(config.TILE_SIZE), int(config.TILE_SIZE)))

    def to_dict(self):
        return {
            "objects": [obj.to_dict() for obj in self.objects.values()],
            "next_id": self.next_id
        }

    def from_dict(self, data):
        self.next_id = data["next_id"]
        self.objects = {}

        for obj in data["objects"]:
            object = FoodDish.from_dict(obj)
            self.objects[obj["id"]] = object

    def get_object_by_id(self, object_id):
        if object_id in self.objects:
            return self.objects[object_id]
        return None

    def add_food_tile(self, pos, enclosure):
        x = pos[0]
        y = pos[1]
        food_dish = FoodDish(x, y, self.next_id)
        food_dish.enclosure_id = enclosure.enclosure_id
        self.objects[self.next_id] = food_dish
        self.tile_index.register_tile(x, y, "food_dish", enclosure.enclosure_id)
        enclosure.food_dishes.append(food_dish)
        self.next_id += 1

    def remove_food_tile(self, id, enclosure):
        if id in self.objects:
            food_dish = self.objects[id]
            self.tile_index.remove_tile(food_dish.pos[0], food_dish.pos[1])
            enclosure.food_dishes.remove(food_dish)
            del self.objects[id]

    def start_placement(self):
        # Sets up hovering state, creates a preview
        if self.state != "HOVERING":
            self.state = "HOVERING"
            self.pending_object = "food_dish"

    def confirm_placement(self, x, y, enclosure = None):
        self.state = "NONE"
        if self.pending_object == "food_dish":
            self.add_food_tile((x,y), enclosure)
            self.pending_object = None

    def cancel_placement(self):
        self.state = "NONE"
        self.pending_object = None

    def draw(self, start_x, start_y):
        if self.state == "HOVERING":
            camera_offset_x = start_x * config.TILE_SIZE
            camera_offset_y = start_y * config.TILE_SIZE
            screenx = self.pending_pos[0] * config.TILE_SIZE - camera_offset_x
            screeny = self.pending_pos[1] * config.TILE_SIZE - camera_offset_y
            self.screen.blit(self.food, (screenx, screeny))


    def update(self, world_mouse_pos):
        if self.state == "HOVERING":
            self.pending_pos = world_mouse_pos