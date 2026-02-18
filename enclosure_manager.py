import pygame
import config
from enclosure import Enclosure
from animal import Animal

class EnclosureManager:
    def __init__(self, screen, tile_index):
        self.enclosures = set()
        self.tile_index = tile_index
        self.next_id = 0
        self.grid_x = 0
        self.grid_y = 0
        self.screen = screen
        self.state = "READY"
        self.fences_remaining = 100

        # Drawing #
        self.selected_enclosure = None
        self.is_drawing = False
        self.hovered_tile = None
        self.hovered_enclosure = None

        # Tile Image #
        self.fence = pygame.image.load('resources/fence.png').convert_alpha()
        self.fence_images = []

        self.sand = pygame.image.load('resources/sand.png').convert()
        self.sand = pygame.transform.scale(self.sand, (int(config.TILE_SIZE), int(config.TILE_SIZE)))

        self.glow_surface = pygame.Surface((config.TILE_SIZE, config.TILE_SIZE))
        self.glow_surface.fill((249, 215, 126)) #((255, 255, 200))

        for y in range(0,3):
            for x in range(0,5):
                self.fence_images.append(self.clip(self.fence, (x,y), 32,32))

        self.fence_images.append(self.clip(self.fence, (0, 3), 32,32))
        self.fence_images.append(self.clip(self.fence, (1,3), 32,32))
        self.fence_images.append(self.clip(self.fence, (2,3), 32,32))

    def update(self, grid_pos, dt): 
        self.grid_x, self.grid_y = grid_pos

        # Check if any other enclosure is selected
        if self.selected_enclosure is None:
            self.hovered_enclosure = self.get_enclosure_at(self.grid_x, self.grid_y)
            for enclosure in self.enclosures:
                is_hovered =  enclosure == self.hovered_enclosure#(enclosure == self.hovered_enclosure if self.selected_enclosure is None else False)
                    # if enclosure.state is not "GLOWING":
                enclosure.update_hover(is_hovered, dt)

        # Handle Drawing #
        if self.is_drawing and self.selected_enclosure and self.get_enclosure_at(self.grid_x, self.grid_y) is None and self.fences_remaining > 0:
            self.selected_enclosure.add_tile(self.grid_x, self.grid_y)
            self.fences_remaining -= 1
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.state == "READY":
                # Select enclosure
                if self.select_enclosure() is not None:
                    self.state = "SELECTED"
            elif self.selected_enclosure.state == "COMPLETE":
                if not self.selected_enclosure.tileWithinEnclosure(self.grid_x, self.grid_y):
                    self.deselect_enclosure()
                        
            else:
                if self.selected_enclosure.state != "COMPLETE":
                   self.startDrawing(self.grid_x, self.grid_y)

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.state == "SELECTED":
               self.finishDrawing()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.state == "SELECTED":
                    self.deselect_enclosure()

            # elif event.key == pygame.K_q:
                # self.animal.find_new_tile()


    def get_enclosure_at(self, x, y):
            for enclosure in self.enclosures:
                if enclosure.tileWithinEnclosure(x, y):
                    return enclosure
            return None
    
    def select_enclosure(self):
        self.selected_enclosure = self.get_enclosure_at(self.grid_x, self.grid_y)

        if self.selected_enclosure is None:
            return None
        else:
            return 1

    def new_enclosure(self):
        self.selected_enclosure = Enclosure(self.next_id, self.tile_index)
        self.enclosures.add(self.selected_enclosure)
        self.next_id += 1
        print("NEW ENCLOSURE")

    def deselect_enclosure(self):
        self.selected_enclosure = None
        self.state = "READY"

    def startDrawing(self, x, y):
        self.is_drawing = True
        print("DRAWING")

    def finishDrawing(self):
        print("FINISH")
        if self.fences_remaining > 0 :
            if self.selected_enclosure and self.selected_enclosure.state != "COMPLETE":
                if self.selected_enclosure.is_closed_loop():
                    self.selected_enclosure._floodBFS(self.selected_enclosure.get_midpoint())
                    print("YES---------------------------")

                    self.selected_enclosure.calculate_fences()

                    self.deselect_enclosure()
                    self.state = "READY"

        self.is_drawing = False

    def clip(self, surface, index, x_size, y_size):
        "Extract a small chunk of the image, index = (x,y)"
        x, y = index
        x *= x_size
        y *= y_size

        handle_surf = surface.copy()

        # Create rect for region that is wanted
        clipR = pygame.Rect(x, y, x_size, y_size)
        
        # Extract subsurface
        image = surface.subsurface(clipR)
        return image.copy()

    def get_enclosureid_at(self, x, y):
        for enclosure in self.enclosures:
            if enclosure.tileWithinEnclosure(x, y):
                return enclosure.enclosure_id

        return None
            
    def draw_enclosures(self, dt, tiles, start_x, start_y):
        camera_offset_x = start_x * config.TILE_SIZE
        camera_offset_y = start_y * config.TILE_SIZE

        # FIRST PASS

        for (tile_x, tile_y), (tile_type, enclosure_id) in tiles.items():
            screenx = tile_x * config.TILE_SIZE - camera_offset_x
            screeny = tile_y * config.TILE_SIZE - camera_offset_y

            enclosure = self.get_enclosure_by_id(enclosure_id)

            if tile_type == "fence":
                # Get fence orientation from enclosure
                image_index = enclosure.fence_orientation.get((tile_x, tile_y), 1)
                self.screen.blit(self.fence_images[image_index], (screenx, screeny))

            elif tile_type == "interior":
                self.screen.blit(self.sand, (screenx, screeny))

                # Glow effect
                self.glow_surface.set_alpha(int(enclosure.glow_intensity * 128))
                self.screen.blit(self.glow_surface, (screenx, screeny))

        # SECOND PASS

        visible_enclosure_ids = {data[1] for data in tiles.values()}
        for enclosure_id in visible_enclosure_ids:
            enclosure = self.get_enclosure_by_id(enclosure_id)

            # Handle glow animation
            if enclosure.state == "FILLING":
                enclosure.update_animation()

            elif enclosure.state == "GLOWING":
                enclosure.update_glow(dt)


        # for enclosure in self.enclosures:
        #     # Draw fence tiles
        #     for tile in enclosure.fence_tiles:
        #         screenx, screeny = tile
        #         screenx = screenx * config.TILE_SIZE
        #         screeny = screeny * config.TILE_SIZE

        #         # if(enclosure.enclosure_id == 0):
        #         image_index = enclosure.fence_orientation.get(tile)
        #         if image_index is None:
        #             image_index = 1

                
        #         self.screen.blit(self.fence_images[image_index], (screenx, screeny))

        #     # Handle glow animation
        #     if enclosure.state == "FILLING":
        #         enclosure.update_animation()

        #     elif enclosure.state == "GLOWING":
        #         enclosure.update_glow(dt)

        #     # Draw interior tiles
        #     for tile in enclosure.interior_tiles:
        #         screenx, screeny = tile
        #         screenx = screenx * config.TILE_SIZE
        #         screeny = screeny * config.TILE_SIZE

        #         self.screen.blit(self.sand, (screenx, screeny))

        #         # Draw glow effect
        #         self.glow_surface.set_alpha(int(enclosure.glow_intensity * 128))
        #         self.screen.blit(self.glow_surface, (screenx, screeny))

    def change_state(self, new_state):
        self.state = new_state

    def get_enclosure_by_id(self, id):
        for enclosure in self.enclosures:
            if enclosure.enclosure_id == id:
                return enclosure
        return None