import config

class Camera:
    """Calculation for world to screen conversion"""
    def __init__(self):
        self.screen_width = config.SCREENWIDTH
        self.screen_height = config.SCREENHEIGHT
        self.x = 0 # World position of camera's top left
        self.y = 0