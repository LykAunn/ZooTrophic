from enclosure_manager import EnclosureManager
from UI.menu_manager import MenuManager
from game_clock import GameClock
from cursor import Cursor
from animal_manager import AnimalManager
import config
import pygame

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.menu_manager = MenuManager(screen, self)
        self.enclosure_manager = EnclosureManager(screen)
        self.game_clock = GameClock()
        self.cursor = Cursor(screen, "resources/cursor.png")
        self.animal_manager = AnimalManager(screen)
        self.mouse_pos = (0,0)

    def update(self, dt, mouse_pos):
        grid_pos = (mouse_pos[0] // config.TILE_SIZE, mouse_pos[1] // config.TILE_SIZE)
        self.mouse_pos = mouse_pos

        game_dt = self.game_clock.update(dt)

        self.enclosure_manager.update(grid_pos, dt)
        self.menu_manager.update(game_dt)
        self.cursor.update(grid_pos[0], grid_pos[1])
        self.animal_manager.update(dt, mouse_pos)

        if self.enclosure_manager.state == "SELECTED":
            if not self.menu_manager.bottom_menu_visible:
                self.menu_manager.show(self.enclosure_manager.selected_enclosure, 1)
                self.menu_manager.hide(2)

        else:
            if self.menu_manager.bottom_menu_visible:
                self.menu_manager.show(None, 2)
                self.menu_manager.hide(1)

    def handle_event(self, event):
        self.menu_manager.bottom_panel.handle_event(event)
        self.menu_manager.bottom_menu.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                self.animal_manager.create_new_animal()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.animal_manager.state == "HOVERING":
                enclosure = self.enclosure_manager.get_enclosure_at(self.mouse_pos[0] // config.TILE_SIZE, self.mouse_pos[1] // config.TILE_SIZE)
                if enclosure is not None:
                    self.animal_manager.start_animal(enclosure)
                else:
                    print("Unable to find enclosure")
            animal = self.animal_manager.get_animal_at(self.mouse_pos)
            if animal:
                self.animal_manager.select_animal(animal)
                self.enclosure_manager.able_to_select = False
                print("SELECT ANIMAL")
                # Give priority to animal. Select animal instead of enclosure
            else:
                self.enclosure_manager.able_to_select = True

        self.enclosure_manager.handle_event(event)
            

    def draw(self, dt):
        self.enclosure_manager.draw_enclosures(dt)
        self.animal_manager.draw()
        if self.animal_manager.state != "HOVERING":
            pygame.mouse.set_visible(True)
            self.cursor.draw_cursor()
        else:
            pygame.mouse.set_visible(False)

        self.menu_manager.draw_menus()

    def on_build_clicked(self):
        self.enclosure_manager.new_enclosure()
        self.enclosure_manager.change_state("SELECTED")
        print(self.enclosure_manager.state)