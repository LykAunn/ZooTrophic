from enclosure_manager import EnclosureManager
from UI.menu_manager import MenuManager
import config

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.menu_manager = MenuManager(screen, self)
        self.enclosure_manager = EnclosureManager(screen)

    def update(self, dt, mouse_pos):
        grid_pos = (mouse_pos[0] // config.TILE_SIZE, mouse_pos[1] // config.TILE_SIZE)

        self.enclosure_manager.update(grid_pos, dt)
        self.menu_manager.update(dt)

        if self.enclosure_manager.selected_enclosure:
            if not self.menu_manager.bottom_visible:
                self.menu_manager.show(self.enclosure_manager.selected_enclosure, 1)
                self.menu_manager.hide(2)

        else:
            if self.menu_manager.bottom_visible:
                self.menu_manager.show(None, 2)
                self.menu_manager.hide(1)

    def handle_event(self, event):
        # if self.menu_manager.handle_event(event):
        #     return
        
        self.enclosure_manager.handle_event(event)
        self.menu_manager.bottom_panel.handle_event(event)
        self.menu_manager.bottom_menu.handle_event(event)
    
    def draw(self, dt):
        self.enclosure_manager.draw_enclosures(dt)
        self.menu_manager.draw_menus()

    def on_build_clicked(self):
        self.enclosure_manager.new_enclosure()
        self.enclosure_manager.change_state("SELECTED")