from UI.bottom_panel import BottomPanel
from UI.top_menu import TopPanel
from UI.bottom_menu import BottomMenu

class MenuManager:
    def __init__(self, screen, game_manager):
        self.screen = screen
        self.game_manager = game_manager
        self.bottom_panel = BottomPanel(screen, game_manager)
        self.top_panel = TopPanel(screen)
        self.bottom_menu = BottomMenu(screen, 80, game_manager)
        self.selected_enclosure = None
        self.top_visible = True
        self.bottom_visible = False

        self.top_panel.show()
        self.bottom_menu.show()

    def show(self, enclosure, whichPanel):
        self.selected_enclosure = enclosure
        if whichPanel == 0:
            self.top_panel.show()
            self.top_visible = True

        elif whichPanel == 1:
            self.bottom_panel.show(enclosure)
            self.bottom_visible = True

        elif whichPanel == 2:
            self.bottom_menu.show()

    def hide(self, whichPanel):
        if whichPanel == 0:
            self.top_panel.hide()
            self.top_visible = False

        elif whichPanel == 1:
            self.bottom_panel.hide()
            self.bottom_visible = False

        elif whichPanel == 2:
            self.bottom_menu.hide()

    def update(self, dt):
        self.bottom_panel.update(dt)
        self.top_panel.update(dt)
        self.bottom_menu.update(dt)

    def draw_menus(self):
        self.bottom_menu.draw()
        self.bottom_panel.draw()
        self.top_panel.draw()