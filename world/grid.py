class Grid:
    def __init__(self):
        self.tile_data = {} # (x,y): {"enclosure:id" : None, "is_fence" : False}
        