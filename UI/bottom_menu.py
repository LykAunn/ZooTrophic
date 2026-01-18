from UI.menu import Menu
import config
from UI.button import Button
from UI.button_icon import ButtonIcon
import pygame

class BottomMenu(Menu):
    def __init__(self, screen, height, game_manager):
        super().__init__(screen, config.SCREENHEIGHT, True, height, config.SCREENHEIGHT, game_manager)

        self.menu_image = pygame.image.load("resources/Bottom_Menu.png").convert_alpha()
        self.menu_image = pygame.transform.scale_by(self.menu_image, config.pixel_size)

        self.state = 0 # 0 = Main , 1 = Contruct
        self.x = (config.SCREENWIDTH / 2) - (self.menu_image.get_width() / 2)

        self.button_set1_config = [("Construct", self.on_construct_clicked), ("Market", game_manager.on_build_clicked),
                               ("Staff", None), ("Research", None), ("Overview", None)]
        
        self.buttonIcon = ButtonIcon("resources/chicken.png", "resources/grass.png", config.SCREENHEIGHT, self.x + 20, self.on_build_clicked)

        # self.build_button = Button(pygame.Rect(20, self.current_y + 20, 100, 20), "Construct", game_manager.on_build_clicked)

        self.firstSet = self.create_button_row(self.button_set1_config, 50)

    def create_button_row(self, button_config, y_offset, button_width = 100, button_height = 20):
        buttons = []
        num_of_buttons = len(button_config)

        menu_width = self.menu_image.get_width() if hasattr(self, 'menu_image') else config.SCREENWIDTH
        spacing = (menu_width - (button_width * num_of_buttons)) / (num_of_buttons + 1)

        for i,(text, callback) in enumerate(button_config):
            x_pos = self.x + (spacing * (i + 1)) + (button_width * i)
            rect = pygame.Rect(x_pos, config.SCREENHEIGHT, button_width, button_height)
            button = Button(rect, text, callback)
            buttons.append(button)

        return buttons

    def update(self, dt):
        super().update(dt)
        for i in range(len(self.firstSet)):
            self.firstSet[i].update_ypos(self.current_y + 50, dt)

        self.buttonIcon.update_ypos(self.current_y + 100, dt)

    def handle_event(self, event):
        if self.is_visible:
            for i in range(len(self.firstSet)):
                self.firstSet[i].handle_event(event)

            if self.state == 1:
                self.buttonIcon.handle_event(event)

    def draw(self):
        self.screen.blit(self.menu_image, (self.x, self.current_y))

        if self.state == 0:

            for i in range (0, len(self.firstSet)):
                self.firstSet[i].draw(self.screen)

        elif self.state == 1:
            self.buttonIcon.draw(self.screen)

    def hide_all_buttons(self, button_set):
        for i in range(0, len(button_set)):
            button_set[i].hide()

    def show_all_buttons(self, button_set):
        for i in range(0, len(button_set)):
            button_set[i].set_target_y(self.target_y + 30)

    def on_construct_clicked(self):
        self.target_y = config.SCREENHEIGHT - self.menu_image.get_height()
        self.state = 1
        self.hide_all_buttons(self.firstSet)
        self.buttonIcon.set_target_y(self.current_y)

    def on_build_clicked(self):
        self.game_manager.on_build_clicked()
        self.buttonIcon.hide()
        self.state = 0

    def show(self):
        super().show()
        for i in range(len(self.firstSet)):
            self.firstSet[i].set_target_y(self.target_y + (self.menu_height / 2))

    def hide(self):
        super().hide()
        self.hide_all_buttons(self.firstSet)