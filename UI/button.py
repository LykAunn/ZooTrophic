import pygame
import config

class Button:
    def __init__(self, rect,text = None,  callback = None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        
        self.hovered = False
        self.pressed = False
        self.visible = True
        self.current_y = self.rect.top
        self.target_y = self.current_y

        self.bg_color = (60,60,60)
        self.hover_color = "green"#(80,80,80)
        self.text_color = (255, 255, 255)
        self.border_color = (100, 100, 100)
        self.border_width = 2

    def handle_event(self, event):
        if self.visible is True:
            if event.type == pygame.MOUSEMOTION:
                self.hovered = self.rect.collidepoint(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.hovered:
                    self.pressed = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.pressed and self.hovered:
                    self.pressed = False
                    if self.callback:
                        return self.callback()
                    else:
                        print("no callback")
                self.pressed = False

    def update_ypos(self, y, dt):
        if abs(self.current_y - self.target_y) > 0.5:
            diff = self.target_y - self.current_y
            self.current_y += diff * config.menu_movement_speed * dt

        else:
            self.current_y = self.target_y

        self.rect.top = self.current_y

    def draw(self, surface):
        if self.current_y >= config.SCREENHEIGHT:
            return
        
        color = self.hover_color if self.hovered else self.bg_color

        pygame.draw.rect(surface, color, self.rect)

        pygame.draw.rect(surface, self.border_color, self.rect , self.border_width)

        font = pygame.font.Font(None, 24)
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def setx(self, x):
        self.rect.left = x
        
    def show(self):
        self.visible = True

    def hide(self):
        self.target_y = config.SCREENHEIGHT

    def set_target_y(self, y):
        self.target_y = y