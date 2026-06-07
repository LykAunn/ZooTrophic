from contextlib import nullcontext

from food_dish import FoodDish
from world.tile_index import TileIndex

class ObjectManager:
    def __init__(self, tile_index):
        self.tile_index = tile_index
        self.objects = {} # Dictionary storing object id as a key and object reference as value
        self.next_id = 0

    def get_object_by_id(self, object_id):
        if object_id in self.objects:
            return self.objects[object_id]
        return None

    def add_food_tile(self, pos, enclosure):
        x = pos[0]
        y = pos[1]
        food_dish = FoodDish(x, y, self.next_id)
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
