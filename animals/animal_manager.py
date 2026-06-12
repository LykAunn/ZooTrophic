from animals.animal import Animal
import config
import pygame

class AnimalManager:
    def __init__(self, screen):
        self.animal_set = set()
        self.next_id = 0
        self.screen = screen
        self.selected_animal = None
        self.state = "IDLE"
        self.clear_menu = None

    def to_dict(self):
        return {
            "animals": [animal.to_dict() for animal in self.animal_set],
            "next_id": self.next_id,
        }

    def from_dict(self, data):
        self.animal_set = set()
        self.next_id = data["next_id"]

        for animal_data in data["animals"]:
            animal = Animal.from_dict(animal_data)
            self.animal_set.add(animal)

    def draw(self, camera_offset):
        if self.animal_set:
            for animal in self.animal_set:
                animal.draw(camera_offset)

        if self.state == "HOVERING" and self.selected_animal is not None:
            self.selected_animal.draw(camera_offset)

    def update(self, dt, mousepos):
        if self.animal_set:
            for animal in self.animal_set:
                animal.update(dt, mousepos)

        if self.state == "HOVERING" and self.selected_animal is not None:
            self.selected_animal.update(dt, mousepos)

    def handle_event(self, event, mouse_pos, camera_offset):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.state == "SELECTED":
                self.deselect_animal()
                return  # consume the click entirely

            animal = self.get_animal_at(mouse_pos, camera_offset)
            if animal is not None:
                self.select_animal(animal)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and self.state == "SELECTED":
                self.deselect_animal()

    def create_new_animal(self):
        self.selected_animal = Animal(self.next_id, None, 0, 0, "chicken", 'resources/chicken.png', 'resources/Chicken_right.png', self.screen)
        self.state = "HOVERING"
        print(self.selected_animal)

    # def select_animal(self, id):
    #     i = 0
    #     animals = list(self.animal_set)
    #     while self.selected_animal.animal_id != id and i < len(self.animal_set):
    #         self.selected_animal = animals[i]
    #         i += 1

    def assign_enclosure(self, enclosure):
        """Assigns currently selected animal to an enclosure. Requires an animal to be selected TODO: implement checks for enclosure type etc"""

        self.selected_animal.set_enclosure(enclosure)

    def start_animal(self, enclosure, world_pos):
        self.assign_enclosure(enclosure)
        self.selected_animal.set_animal_tile(world_pos)
        self.selected_animal.find_new_tile()
        self.selected_animal.start_moving()
        enclosure.animals_in_enclosure += 1

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

    def get_animal_at(self, mouse_pos, camera_offset):
        """Locates animal based on mouse_pos parameter. mouse_pos is a tuple with x and y"""
        for animal in self.animal_set:
            # Check if mouse is within animal sprite bounds
            screen_x = animal.world_pixel_coords[0] - camera_offset[0] * config.TILE_SIZE
            screen_y = animal.world_pixel_coords[1] - camera_offset[1] * config.TILE_SIZE
            right = screen_x + config.TILE_SIZE * 1.5
            bottom = screen_y + config.TILE_SIZE * 1.5

            if screen_x <= mouse_pos[0] <= screen_x + config.TILE_SIZE * 1.5 and \
                screen_y <= mouse_pos[1] <= screen_y + config.TILE_SIZE * 1.5:
                return animal
        
        print("NONE")
        return None
    
    def select_animal(self, animal):
        self.selected_animal = animal
        self.state = "SELECTED"