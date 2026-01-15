from UI.menu import Menu
import config
from UI.button import Button
import pygame

class BottomMenu(Menu):
    def __init__(self, screen, height, game_manager):
        super().__init__(screen, config.SCREENHEIGHT, True, height, config.SCREENHEIGHT, game_manager)

        self.menu_image = pygame.image.load("resources/Bottom_Menu.png").convert_alpha()
        self.menu_image = pygame.transform.scale_by(self.menu_image, config.pixel_size)

        self.state = 0 # 0 = Main , 1 = Contruct
        self.x = (config.SCREENWIDTH / 2) - (self.menu_image.get_width() / 2)
        
        self.construct_button = Button(pygame.Rect(20, self.current_y + 20, 100, 20), "Construct", self.on_construct_clicked)
        self.market_button = Button(pygame.Rect(20, self.current_y + 20, 100, 20), "Market", game_manager.on_build_clicked)
        self.staff_button = Button(pygame.Rect(20, self.current_y + 20, 100, 20), "Staff", None)
        self.research_button = Button(pygame.Rect(20, self.current_y + 20, 100, 20), "Research", None)
        self.overview_button = Button(pygame.Rect(20, self.current_y + 20, 100, 20), "Overview", None)
        self.firstSet = [self.construct_button, self.market_button, self.staff_button, self.research_button, self.overview_button]

        # self.build_button = Button(pygame.Rect(20, self.current_y + 20, 100, 20), "Construct", game_manager.on_build_clicked)

        self.spacing = (self.menu_image.get_width() - (100 * len(self.firstSet))) / (len(self.firstSet) + 1)

        for i in range (0, len(self.firstSet)):
            self.firstSet[i].setx(self.x + (self.spacing * (i + 1)) + (100 * i))

    def update(self, dt):
        super().update(dt)
        for i in range(len(self.firstSet)):
            self.firstSet[i].update_ypos(self.current_y + 20)

    def handle_event(self, event):
        if self.is_visible:
            for i in range(len(self.firstSet)):
                self.firstSet[i].handle_event(event)

    def draw(self):
        self.screen.blit(self.menu_image, (self.x, self.current_y))

        if self.state == 0:

            for i in range (0, len(self.firstSet)):
                self.firstSet[i].draw(self.screen)

    def on_construct_clicked(self):
        self.state = 1