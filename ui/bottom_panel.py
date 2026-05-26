import pygame
import config
from animals.animal import Animal
from ui.menu import Menu
from ui.button import Button
from enclosures.enclosure import Enclosure
from core.states import States

class BottomPanel(Menu):
    def __init__(self, screen, game_manager):
        super().__init__(screen, config.SCREENHEIGHT, False, 80, config.SCREENHEIGHT, game_manager)

        # Logic
        self.selected_enclosure = None
        self.selected_animal = None
        self.panel_state = States.EMPTY
        self.hide_timer = 0
        self.hide_wait_time = 2

        # Button
        self.buttons = []
        self.button = Button(pygame.Rect(300, self.current_y + 25, 100, 20), "BUILD")

        # Sprite
        self.menu_image = pygame.image.load("resources/Bottom_Menu.png").convert_alpha()
        self.menu_image = pygame.transform.scale_by(self.menu_image, config.pixel_size)
        self.menu_x = (config.SCREENWIDTH / 2) - (self.menu_image.get_width() / 2)

        self.bar_image = pygame.image.load("resources/bar.png").convert_alpha()
        self.bar_image = pygame.transform.scale_by(self.bar_image, config.pixel_size)
        self.bar_width = self.bar_image.get_width()
        self.bar_height = self.bar_image.get_height()

        # Font
        self.time_text = "None"
        self.date_text = "None"
        try:  # Try to load font
            self.font = pygame.font.Font('resources/font.ttf', 20)
        except FileNotFoundError:
            print("Font not found, using default.")
            self.font = pygame.font.Font(None, 20)

        # Text
        #self.

    def show(self, subject):
        if isinstance(subject, Enclosure):
            self.panel_state = States.ENCLOSURE
            self.selected_enclosure = subject
            self.selected_animal = None

        elif isinstance(subject, Animal):
            self.panel_state = States.ANIMAL
            self.selected_animal = subject
            self.selected_enclosure = None

        self.target_y = config.SCREENHEIGHT - self.menu_image.get_height()#self.menu_height
        self.is_visible = True

    def hide(self):
        super().hide()
        self.panel_state = States.TRANSITION
        self.hide_timer = 0

    def draw(self):
        if self.current_y >= config.SCREENHEIGHT:
            return
        
        self.screen.blit(self.menu_image, (self.menu_x, self.current_y))

        self.button.draw(self.screen)

        if self.panel_state == States.ANIMAL or (self.panel_state == States.TRANSITION and self.selected_animal is not None):
            self.draw_inverse_stat_bar(self.menu_x + 100, self.current_y + 83, self.bar_width, self.bar_height, self.selected_animal.get_hunger())
            self.draw_inverse_stat_bar(self.menu_x + 100, self.current_y + 113, self.bar_width, self.bar_height, self.selected_animal.get_thirst())

    def update(self, dt):
        super().update(dt)
        self.button.update_ypos(self.current_y + 25, dt)
        if self.panel_state == States.TRANSITION:
            self.timer_countdown(dt)

    def handle_event(self, event):
        self.button.handle_event(event)

    def draw_stat_bar(self, x, y, width, height, animal_value):
        """animal_value = tuple with value and max value"""
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, width, height))
        percentage = animal_value[0] / animal_value[1]
        bar_width = width * percentage
        color = (68, 112, 45)

        if percentage < 0.5:
            if percentage < 0.3:
                color = (181, 89, 69)
            else:
                color = (222, 159, 71)

        pygame.draw.rect(self.screen, color, (x, y, bar_width, height))

    def draw_inverse_stat_bar(self, x, y, width, height, animal_value):
        self.screen.blit(self.bar_image, (x, y))
        percentage = animal_value[0] / animal_value[1]
        bar_width = width * percentage
        color = (68, 112, 45)

        if percentage > 0.65:
            if percentage > 0.8:
                color = (181, 89, 69)
            else:
                color = (222, 159, 71)

        pygame.draw.rect(self.screen, color, (x, y, bar_width, height))

    def timer_countdown(self, dt):
        self.hide_timer += dt
        if self.hide_timer > self.hide_wait_time:
            self.panel_state = States.EMPTY
            self.selected_enclosure = None
            self.selected_animal = None