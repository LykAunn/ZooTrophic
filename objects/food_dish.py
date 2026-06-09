import math


class FoodDish:
    def __init__(self, x, y, id):
        self.position = (x,y)
        self.id = id
        self.food_amount = 1
        self.max_food_amount = 50
        self.is_empty = False

    def eat(self, amount):
        if self.is_empty:
            return False

        self.food_amount -= amount
        print("FOOD AMOUNT: ", self.food_amount)
        if self.food_amount <= 0:
            self.food_amount = 0
            self.is_empty = True
        return True

    def replenish(self, amount):
        new_amount = amount + self.food_amount
        if not new_amount > self.max_food_amount:
            self.food_amount = new_amount

    def distance_to(self, animal_pos):
        return (self.position[0] - animal_pos[0])**2 + (self.position[1] - animal_pos[1])**2