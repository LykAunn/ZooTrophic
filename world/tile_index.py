class TileIndex:
    """Tile data storage"""
    def __init__(self):
        self.tiles = {}

    def register_tile(self, x, y, tile_type, enclosure_id = None):
        """Add tile data into TileIndex. Type of tile and optionally enclosure_id for enclosure tile is bounded to"""
        self.tiles[(x, y)] = (tile_type, enclosure_id)

    def unregister_tile(self, x, y):
        """Remove tile from TileIndex eg, deleting an enclosure"""
        self.tiles.pop((x,y), None)

    def get_tile(self, x, y):
        return self.tiles.get((x,y)) # Returns None if empty
    
    def is_occupied(self, x, y):
        return (x,y) in self.tiles
    
    def get_tiles_in_range(self, start_x, start_y, end_x, end_y):
        # print(f"Range: x({start_x} to {end_x}), y({start_y} to {end_y})")
        # print(f"All tiles in index: {list(self.tiles.keys())}")
        result =  {
            pos: data
            for pos, data in self.tiles.items()
                if start_x <= pos[0] < end_x and start_y <= pos[1] <= end_y
        }

        # print(f"Tiles in range: {list(result.keys())}")
        return result
