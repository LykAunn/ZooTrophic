from animal import Animal
import config
import pygame

class AnimalManager:
    def __init__(self, screen):
        self.animal_set = set()
        self.next_id = 0
        self.screen = screen
        self.selected_animal = None
        self.state = "IDLE"

    def draw(self):
        if self.animal_set:
            for animal in self.animal_set:
                animal.draw()

        if self.state == "HOVERING" and self.selected_animal is not None:
            self.selected_animal.draw()

    def update(self, dt, mousepos):
        if self.animal_set:
            for animal in self.animal_set:
                animal.update(dt, mousepos)

        if self.state == "HOVERING" and self.selected_animal is not None:
            self.selected_animal.update(dt, mousepos)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.state == "SELECTED":
                    self.deselect_animal()

    def create_new_animal(self):
        self.selected_animal = Animal(self.next_id, None, 0, 0, "chicken", 'resources/chicken.png', 'resources/Chicken_right.png',self.screen)
        self.state = "HOVERING"
        print(self.selected_animal)

    def select_animal(self, id):
        i = 0
        animals = list(self.animal_set)
        while self.selected_animal.animal_id != id and i < len(self.animal_set):
            self.selected_animal = animals[i]
            i += 1

    def assign_enclosure(self, enclosure):
        """Assigns currently selected animal to an enclosure. Requires an animal to be selected TODO: implement checks for enclosure type etc"""

        self.selected_animal.set_enclosure(enclosure)

    def start_animal(self, enclosure):
        self.assign_enclosure(enclosure)
        coords = tuple(c // config.TILE_SIZE for c in self.selected_animal.screen_coords)
        self.selected_animal.set_animal_tile(coords)
        self.selected_animal.find_new_tile()
        self.selected_animal.start_moving()

        # Add to set
        self.animal_set.add(self.selected_animal)
        self.next_id += 1

        self.deselect_animal()
    
    def cancel_placement(self):
        """Cancels placement (discard reference)"""
        self.selected_animal = None
        self.state = "IDLE"

    def deselect_animal(self):
        self.selected_animal = None
        self.state = "IDLE"

    def get_animal_at(self, mouse_pos):
        """Locates animal based on mouse_pos parameter. mouse_pos is a tuple with x and y"""
        for animal in self.animal_set:
            # Check if mouse is within animal sprite bounds
            left = animal.screen_coords[0]
            top = animal.screen_coords[1]
            right = left + config.TILE_SIZE
            bottom = top + config.TILE_SIZE

            if left <= mouse_pos[0] <= right and top <= mouse_pos[1] <= bottom:
                print("FOUND ANIMAL")
                return animal
        
        print("NONE")
        return None
    
    def select_animal(self, animal):
        self.selected_animal = animal
        self.state = "SELECTED"