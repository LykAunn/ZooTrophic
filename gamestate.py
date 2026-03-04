from enclosure_manager import EnclosureManager
from UI.menu_manager import MenuManager
from game_clock import GameClock
from cursor import Cursor
from animal_manager import AnimalManager
from UI.clock_menu import ClockMenu
from player import Player
from terrain import TerrainRenderer
from tile_index import TileIndex
import config
import pygame
import pygame.gfxdraw
from decimal import Decimal

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.mouse_pos = (0,0)
        self.player_coords = (0,0)
        self.top_left_player_coords = (0,0)
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

    def update(self, dt, mouse_pos):
        grid_pos = (mouse_pos[0] // config.TILE_SIZE, mouse_pos[1] // config.TILE_SIZE)
        self.mouse_pos = mouse_pos

        game_dt = self.game_clock.update(dt)

        # Player
        self.player.update(dt)
        self.player_coords = self.player.get_position()

        # Camera calculation (Integer for logic, float for movement)
        self.top_left_player_coords = self.player_coords[0] - self.boundary_x, self.player_coords[1] - self.boundary_y
        world_grid_pos = self.screen_to_world_tile(mouse_pos)

        # Game logic
        self.enclosure_manager.update(world_grid_pos, dt)
        self.menu_manager.update(game_dt)
        self.animal_manager.update(dt, mouse_pos)

        # UI
        self.cursor.update(mouse_pos, self.top_left_player_coords)
        self.clock_menu.update(dt)

        if self.enclosure_manager.state == "SELECTED":
            if not self.menu_manager.bottom_menu_visible:
                self.menu_manager.show(self.enclosure_manager.selected_enclosure, 1)
                self.menu_manager.hide(2)

        elif self.animal_manager.state == "SELECTED":
            if not self.menu_manager.bottom_menu_visible:
                self.menu_manager.show(None, 1)
                self.menu_manager.hide(2)

        else:
            if self.menu_manager.bottom_menu_visible:
                self.menu_manager.show(None, 2)
                self.menu_manager.hide(1)

    def handle_event(self, event):
        self.menu_manager.bottom_panel.handle_event(event)
        self.menu_manager.bottom_menu.handle_event(event)
        self.animal_manager.handle_event(event)

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
                enclosure = self.enclosure_manager.get_enclosure_at(self.mouse_pos[0] // config.TILE_SIZE, self.mouse_pos[1] // config.TILE_SIZE)
                if enclosure is not None:
                    self.animal_manager.start_animal(enclosure)
                else:
                    print("Unable to find enclosure")
                return # Stop processing the click
            
            # Only check for animal selection if not hovering
            animal = self.animal_manager.get_animal_at(self.mouse_pos)
            if animal is not None:
                self.animal_manager.select_animal(animal)
                self.enclosure_manager.able_to_select = False
                print("SELECT ANIMAL")
                # Give priority to animal. Select animal instead of enclosure
                return
                
        # Only select enclosure if no animal was clicked
        if self.animal_manager.state == "IDLE":
            self.enclosure_manager.handle_event(event)

    def draw(self, dt):
        # Bounds calculation
        tiles = self.tile_index.get_tiles_in_range(self.player_coords[0] - self.boundary_x - 1, self.player_coords[1] - self.boundary_y,
                                                self.player_coords[0] + self.boundary_x, self.player_coords[1] + self.boundary_y)

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

        # UI
        self.menu_manager.draw_menus()
        self.clock_menu.draw(self.screen)

    def screen_to_world_tile(self, mouse_pos):
        """Convert screen mouse position to world tile coordinates."""
        # Fractional camera offset in pixels
        offset_x = (self.top_left_player_coords[0] % 1) * config.TILE_SIZE
        offset_y = (self.top_left_player_coords[1] % 1) * config.TILE_SIZE

        # Which screen tile is under the mouse (accounting for visual offset)
        screen_tile_x = (mouse_pos[0] + offset_x) // config.TILE_SIZE
        screen_tile_y = (mouse_pos[1] + offset_y) // config.TILE_SIZE

        # Convert to world tile
        world_tile_x = int(screen_tile_x + self.top_left_player_coords[0])
        world_tile_y = int(screen_tile_y + self.top_left_player_coords[1])

        return (world_tile_x, world_tile_y)

    def on_build_clicked(self):
        self.enclosure_manager.new_enclosure()
        self.enclosure_manager.change_state("SELECTED")
        print(self.enclosure_manager.state)