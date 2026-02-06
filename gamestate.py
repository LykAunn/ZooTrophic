from enclosure_manager import EnclosureManager
from UI.menu_manager import MenuManager
from game_clock import GameClock
from cursor import Cursor
from animal import Animal
import config

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.menu_manager = MenuManager(screen, self)
        self.enclosure_manager = EnclosureManager(screen)
        self.game_clock = GameClock()
        self.cursor = Cursor(screen, "resources/cursor.png")

    def update(self, dt, mouse_pos):
        grid_pos = (mouse_pos[0] // config.TILE_SIZE, mouse_pos[1] // config.TILE_SIZE)

        game_dt = self.game_clock.update(dt)

        self.enclosure_manager.update(grid_pos, dt)
        self.menu_manager.update(game_dt)
        self.cursor.update(grid_pos[0], grid_pos[1])

        if self.enclosure_manager.selected_enclosure:
            if not self.menu_manager.bottom_menu_visible:
                self.menu_manager.show(self.enclosure_manager.selected_enclosure, 1)
                self.menu_manager.hide(2)

        else:
            if self.menu_manager.bottom_menu_visible:
                self.menu_manager.show(None, 2)
                self.menu_manager.hide(1)


    def handle_event(self, event):
        # if self.menu_manager.handle_event(event):
        
        self.enclosure_manager.handle_event(event)
        self.menu_manager.bottom_panel.handle_event(event)
        self.menu_manager.bottom_menu.handle_event(event)
    
    def draw(self, dt):
        self.enclosure_manager.draw_enclosures(dt)
        self.cursor.draw_cursor()
        self.menu_manager.draw_menus()

    def on_build_clicked(self):
        self.enclosure_manager.new_enclosure()
        self.enclosure_manager.change_state("SELECTED")