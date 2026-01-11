import pygame
import config
from enclosure import Enclosure

class EnclosureManager:
    def __init__(self, screen):
        self.enclosures = set()
        self.next_id = 0
        self.grid_x = 0
        self.grid_y = 0
        self.screen = screen
        self.state = "READY"

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
        if self.is_drawing and self.selected_enclosure and self.get_enclosure_at(self.grid_x, self.grid_y) is None:
            self.selected_enclosure.add_tile(self.grid_x, self.grid_y)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.state == "READY":
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

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.state == "SELECTED":
                self.deselect_enclosure()
                print("!!!!!!!!!!!DESELECT")

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

        # if self.selected_enclosure is None:
        #     self.selected_enclosure = Enclosure(self.next_id)
        #     self.enclosures.add(self.selected_enclosure)
        #     self.next_id += 1
        #     print("NEW ENCLOSURE")

    def new_enclosure(self):
        self.selected_enclosure = Enclosure(self.next_id)
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
        if self.selected_enclosure and self.selected_enclosure.state != "COMPLETE":
            if self.selected_enclosure.is_closed_loop():
                print(self.selected_enclosure._floodBFS(self.selected_enclosure.get_midpoint()))
                print("YES---------------------------")
                self.selected_enclosure.calculate_fences()
                # self.selected_enclosure.set_state_to("FILLING")
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
            
    def draw_enclosures(self, dt):
        for enclosure in self.enclosures:
            # Draw fence tiles
            for tile in enclosure.fence_tiles:
                screenx, screeny = tile
                screenx = screenx * config.TILE_SIZE
                screeny = screeny * config.TILE_SIZE

                # if(enclosure.enclosure_id == 0):
                image_index = enclosure.fence_orientation.get(tile)
                if image_index is None:
                    image_index = 1

                
                self.screen.blit(self.fence_images[image_index], (screenx, screeny))

            # Handle glow animation
            if enclosure.state == "FILLING":
                enclosure.update_animation()

            elif enclosure.state == "GLOWING":
                enclosure.update_glow(dt)

            # Draw interior tiles
            for tile in enclosure.interior_tiles:
                screenx, screeny = tile
                screenx = screenx * config.TILE_SIZE
                screeny = screeny * config.TILE_SIZE

                self.screen.blit(self.sand, (screenx, screeny))

                # Draw glow effect
                # if (enclosure.state == "GLOWING"):
                self.glow_surface.set_alpha(int(enclosure.glow_intensity * 128))

                self.screen.blit(self.glow_surface, (screenx, screeny))

            # if self.state == "SELECTED":

    def change_state(self, newState):
        self.state = newState