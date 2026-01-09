from bottom_panel import BottomPanel
from top_panel import TopPanel

class MenuManager:
    def __init__(self, screen):
        self.screen = screen
        self.bottom_panel = BottomPanel(screen)
        self.top_panel = TopPanel(screen)
        self.selected_enclosure = None
        self.top_visible = True
        self.bottom_visible = False

        self.top_panel.show()

    def show(self, enclosure, whichPanel):
        self.selected_enclosure = enclosure
        if whichPanel == 0:
            self.top_panel.show()
            self.top_visible = True

        elif whichPanel == 1:
            self.bottom_panel.show(enclosure)
            self.bottom_visible = True

    def hide(self, whichPanel):
        if whichPanel == 0:
            self.top_panel.hide()
            self.top_visible = False

        if whichPanel == 1:
            self.bottom_panel.hide()
            self.bottom_visible = False

    def update(self, dt):
        self.bottom_panel.update(dt)
        self.top_panel.update(dt)

    def draw_menus(self):
        self.bottom_panel.draw()
        self.top_panel.draw()