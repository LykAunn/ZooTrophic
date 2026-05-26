from world.camera import Camera
from enclosures.enclosure_manager import EnclosureManager
from ui.menu_manager import MenuManager
from core.game_clock import GameClock
from player.cursor import Cursor
from animals.animal_manager import AnimalManager
from ui.clock_menu import ClockMenu
from player.player import Player
from world.terrain import TerrainRenderer
from world.tile_index import TileIndex
import config
import pygame
import pygame.gfxdraw


class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.mouse_pos = (0,0)
        self.player_coords = (0,0)
        self.top_left_player_coords = (0,0)
        self.world_mouse_pos = (0,0)
        self.boundary_x = config.noOfTiles_x // 2
        self.boundary_y = config.noOfTiles_y // 2

        # Class References
        self.tile_index = TileIndex()
        self.menu_manager = MenuManager(screen, self)
        self.enclosure_manager = EnclosureManager(screen, self.tile_index)
        self.game_clock = GameClock()
        self.cursor = Cursor(screen, "resources/cursor.png")
        self.animal_manager = AnimalManager(screen)
        self.clock_menu = ClockMenu(50,50,50, self.game_clock)
        self.player = Player()
        self.game_clock.register_hour_listener(self.clock_menu.increment_hour)
        self.terrain_generator = TerrainRenderer(self.screen)
        self.camera = Camera()
        self.enclosure_manager.clear_menu = self.clear_menu
        self.animal_manager.clear_menu = self.clear_menu

    def update(self, dt, mouse_pos):
        grid_pos = (mouse_pos[0] // config.TILE_SIZE, mouse_pos[1] // config.TILE_SIZE)
        self.mouse_pos = mouse_pos

        game_dt = self.game_clock.update(dt)

        # Player
        self.player.update(dt)
        self.player_coords = self.player.get_position()

        # Camera calculation (Integer for logic, float for movement)
        self.top_left_player_coords = self.player_coords[0] - self.boundary_x, self.player_coords[1] - self.boundary_y
        self.world_mouse_pos = self.camera.screen_to_world_tile(mouse_pos, self.top_left_player_coords)

        # Game logic
        self.enclosure_manager.update(self.world_mouse_pos, dt)
        self.menu_manager.update(dt)
        self.animal_manager.update(game_dt, mouse_pos)

        # ui
        self.cursor.update(mouse_pos, self.top_left_player_coords)
        self.clock_menu.update(dt)

        # if self.enclosure_manager.state == "SELECTED":
        #     if not self.menu_manager.bottom_menu_visible:
        #         self.menu_manager.show(self.enclosure_manager.selected_enclosure, 1)
        #         self.menu_manager.hide(2)
        #
        # elif self.animal_manager.state == "SELECTED":
        #     if not self.menu_manager.bottom_menu_visible:
        #         self.menu_manager.show(None, 1)
        #         self.menu_manager.hide(2)
        #
        # else:
        #     if self.menu_manager.bottom_menu_visible:
        #         self.menu_manager.show(None, 2)
        #         self.menu_manager.hide(1)

    def handle_event(self, event):
        self.menu_manager.bottom_panel.handle_event(event)
        self.menu_manager.bottom_menu.handle_event(event)
        self.animal_manager.handle_event(event)
        self.clock_menu.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                self.animal_manager.create_new_animal()
            elif event.key == pygame.K_ESCAPE:
                if self.animal_manager.state == "HOVERING":
                    self.animal_manager.cancel_placement()
            elif event.key == pygame.K_1:
                if not self.game_clock.paused:
                    self.game_clock.pause()
                else:
                    self.game_clock.unpause()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.animal_manager.state == "HOVERING":
                enclosure = self.enclosure_manager.get_enclosure_at(self.world_mouse_pos[0], self.world_mouse_pos[1])
                if enclosure is not None:
                    self.animal_manager.start_animal(enclosure, self.world_mouse_pos)
                else:
                    print("Unable to find enclosure")
                return # Stop processing the click
            
            # Only check for animal selection if not hovering
            animal = self.animal_manager.get_animal_at(self.mouse_pos, self.top_left_player_coords)
            if animal is not None:
                self.animal_manager.select_animal(animal)
                self.menu_manager.on_animal_selected(animal)
                self.enclosure_manager.able_to_select = False
                print("SELECT ANIMAL")
                # Give priority to animal. Select animal instead of enclosure
                return
                
        # Only select enclosure if no animal was clicked
        if self.animal_manager.state == "IDLE":
            self.enclosure_manager.handle_event(event)
            enclosure = self.enclosure_manager.selected_enclosure
            if enclosure: self.menu_manager.on_enclosure_selected(enclosure)

    def draw(self, dt):
        # Bounds calculation
        tiles = self.tile_index.get_tiles_in_range(self.player_coords[0] - self.boundary_x - 1, self.player_coords[1] - self.boundary_y -1,
                                                self.player_coords[0] + self.boundary_x + 1, self.player_coords[1] + self.boundary_y + 1)

        end_x = self.top_left_player_coords[0] + config.noOfTiles_x + 1
        end_y = self.top_left_player_coords[1] + config.noOfTiles_y + 1

        # Terrain
        self.terrain_generator.draw(self.top_left_player_coords, end_x, end_y)

        # Enclosure Tiles
        self.enclosure_manager.draw_enclosures(dt, tiles, self.top_left_player_coords[0], self.top_left_player_coords[1])

        # Animals
        self.animal_manager.draw(self.top_left_player_coords)

        # Cursor
        if self.animal_manager.state != "HOVERING":
            pygame.mouse.set_visible(True)
            self.cursor.draw_cursor()
        else:
            pygame.mouse.set_visible(False)

        # ui
        self.menu_manager.draw_menus()
        self.clock_menu.draw(self.screen)

    def on_build_clicked(self):
        self.enclosure_manager.new_enclosure()
        self.enclosure_manager.change_state("DRAWING")

    def clear_menu(self):
        self.menu_manager.on_selection_cleared()