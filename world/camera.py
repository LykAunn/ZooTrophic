import config

class Camera:
    """Calculation for world to screen conversion"""
    def __init__(self):
        self.screen_width = config.SCREENWIDTH
        self.screen_height = config.SCREENHEIGHT
        self.x = 0 # World position of camera's top left
        self.y = 0

    def screen_to_world_tile(self, mouse_pos, top_left_player_coords):
        """Convert screen mouse position to world tile coordinates."""
        # Fractional camera offset in pixels
        offset_x = (top_left_player_coords[0] % 1) * config.TILE_SIZE
        offset_y = (top_left_player_coords[1] % 1) * config.TILE_SIZE

        # Which screen tile is under the mouse (accounting for visual offset)
        screen_tile_x = (mouse_pos[0] + offset_x) // config.TILE_SIZE
        screen_tile_y = (mouse_pos[1] + offset_y) // config.TILE_SIZE

        negative_offset_x = -1 if top_left_player_coords[0] < 0 else 0
        negative_offset_y = -1 if top_left_player_coords[1] < 0 else 0

        # Convert to world tile
        world_tile_x = int(screen_tile_x + top_left_player_coords[0] + negative_offset_x)
        world_tile_y = int(screen_tile_y + top_left_player_coords[1] + negative_offset_y)

        # print(f"Player: {top_left_player_coords[0]}, {top_left_player_coords[1]}")
        # print(f"Tile: {screen_tile_x}, {screen_tile_y}")
        # print(f"World: {world_tile_x}, {world_tile_y}")

        return world_tile_x, world_tile_y