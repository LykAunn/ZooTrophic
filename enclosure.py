import config
import math

class Enclosure:
    def __init__(self, enclosure_id):
        self.enclosure_id = enclosure_id
        self.fence_tiles = set() # set of (x,y) tuples of the coordinates of the fence tiles
        self.interior_tiles = set()
        self.biome_type = "Grassland"
        self.color = (100, 200, 255)
        self.animals = []
        self.state = "READY"
        self.fill_queue = []
        self.fence_orientation = {}

        # GLOW #
        self.glow_timer = 0
        self.glow_intensity = 0
        self.target_glow = 0

    def tileWithinEnclosure(self, x, y):
        return ((x,y) in self.fence_tiles or (x, y) in self.interior_tiles)
    
    def add_tile(self, x, y):
        self.fence_tiles.add((x, y))

    def get_adjacent_fence_tiles(self, x, y):
        adjacent_tiles = ((x - 1, y) , (x + 1, y) , (x, y + 1) , (x, y - 1), (x + 1, y+ 1), (x + 1, y - 1), (x - 1, y+ 1), (x -1, y -1))
        adjacent_fence_tiles = set()

        # Check the 4 possible adjacent tiles if it is a fence tile
        for tile in adjacent_tiles:
            if tile in self.fence_tiles:
                adjacent_fence_tiles.add(tile)

        return adjacent_fence_tiles
    
    def _traverse(self, x, y, start_x, start_y, visited, is_first_iteration):
        # If it has found the starting tile
        if not is_first_iteration and (x,y) == (start_x, start_y):
            return True
        
        # Else add the fence tile to visited set
        visited.add((x,y))
        print(f"Visiting: {x}, {y}")
        print(f"Visited so far: {visited}")

        # Recursively call function to check all possible adjacent tiles
        for nx, ny in self.get_adjacent_fence_tiles(x, y):
            if (nx, ny) == (start_x, start_y) and not is_first_iteration:
                if len(visited) > len(self.fence_tiles) / 1.5 :
                    return True
            elif (nx, ny) not in visited:
                if self._traverse(nx, ny, start_x, start_y, visited, False):
                    return True
                
        return False
    
    def is_closed_loop(self):
        # Loop not closed / loop to small
        if len(self.fence_tiles) < 4:
            return False
        
        # Pick any fence as starting tile
        start_x, start_y = next(iter(self.fence_tiles))

        visited = set()
        visited.add((start_x, start_y))
        print(f"Start x,y: {start_x}, {start_y}")
        
        for nx, ny in self.get_adjacent_fence_tiles(start_x, start_y):
          if self._traverse(nx, ny, start_x, start_y, visited, True):
              if len(visited) > len(self.fence_tiles) / 1.5:
                  return True
        return False
        
    def get_midpoint(self):
        x = 0
        y = 0
        for tile in self.fence_tiles:
            x += tile[0]
            y += tile[1]

        x = x // len(self.fence_tiles)
        y = y // len(self.fence_tiles)

        return (x, y)
    
    def recursive_check(self, location, visited):
        if location in self.fence_tiles or location in visited:
            return
        
        #TODO: Either check tile data for other enclosure that is within the enclosure or iterate through all the enclosures to check.

        visited.append(location)

        x, y = location

        self.recursive_check((x + 1, y))
        self.recursive_check((x - 1, y))
        self.recursive_check((x, y + 1))
        self.recursive_check((x, y - 1))

    def check_for_overlap(self):
        visited = set()

        return self.recursive_check(self.get_midpoint(), visited)

    def _floodBFS(self, location):
        self.state = "FILLING"
        queue = [location]
        visited = set()
        x, y = location

        # Start BFS
        while queue:
            current = queue.pop(0)

            if x < 0 or y < 0 or x >= 40 or y >= 40:
                continue

            # If hit a wall or other filled tiles
            if current in visited or current in self.fence_tiles:
                continue
             
            visited.add(current)
            self.fill_queue.append(current)

            x, y = current

            queue.append((x + 1, y))
            queue.append((x - 1, y))
            queue.append((x, y + 1))
            queue.append((x, y - 1))

    def update_animation(self):
        if not self.fill_queue:
            self.state = "GLOWING"
            self.glow_timer = 0

        if self.state == "FILLING":
            for _ in range(0, config.fill_speed):
                if not self.fill_queue:
                    break

                coords = self.fill_queue.pop(0)

                self.interior_tiles.add(coords)

    def update_glow(self, dt):
        self.glow_timer += dt

        if self.glow_timer > config.glow_duration:
            self.state = "COMPLETE"

        intensity_progress = self.glow_timer / config.glow_duration
        self.glow_intensity = math.sin(intensity_progress * math.pi)
        # self.glow_intensity = abs(math.sin(self.glow_timer * 3))

    def update_hover(self, is_hovered, dt):
        self.target_glow = 1.0 if is_hovered else 0.0

        glow_speed = 7
        difference = self.target_glow - self.glow_intensity
        self.glow_intensity += difference * glow_speed * dt

        self.glow_intensity = max(0.0, min(1.0, self.glow_intensity))

    def get_connections(self, location):
        x, y = location
        connections = 0
        directions = [(-1, -1), (0, -1), (1,-1), 
                      (-1, 0),            (1, 0), 
                      (-1, 1), (0, 1), (1,1)]

        for i, (dx, dy) in enumerate(directions):
            if (x + dx, y + dy) in self.fence_tiles:
                connections |= (1 << i)
        
        return connections
    
    def match_pattern(self, connection, mask, pattern):
        return (connection & mask) == pattern
    
    def get_fence_sprite_index(self, location):
        connection = self.get_connections(location)
        sprite_map = {
            # 0x30: 10,
            0x88: 2,
            0x24: 10,
            0x81: 11,
            # 0x11: 13,
            # 0xC: 11,
            0x18: 1,
            # 0x42: 12,
            # 0x41: 8,
            # 0x44: 3,
            0x50 : 0,
            0x21 : 14,
            0x84 :17
        }

        index = sprite_map.get(connection)

        if index:
            return index

        masked_patterns = {
            (0x7E, 0x48) : 5,
            (0xDB, 0x50) : 0,
            (0xDB, 0xA) : 6,
            (0x7E, 0x12) : 7,
            (0x7F, 0x11) : 16,
            (0xDE, 0xC) : 13,
            (0x5A, 0x42) : 15,
            (0xFB, 0x30) : 12,
            (0xFA, 0x22) : 4,
            (0xFA, 0x82) : 9,
            (0x5F, 0x44) : 3,
            (0x5F, 0x41) : 8
        }

        for (mask, pattern), sprite_index in masked_patterns.items():
            if self.match_pattern(connection, mask, pattern):
                return sprite_index
            
        return 1
    
    def calculate_fences(self):
        for location in self.fence_tiles:
            self.fence_orientation.update({location: self.get_fence_sprite_index(location)})

    def set_state_to(self, state):
        self.state = state