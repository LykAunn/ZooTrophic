import pygame
import config
from enclosure_manager import EnclosureManager


# Setup
pygame.init()
screen = pygame.display.set_mode((config.SCREENWIDTH,config.SCREENHEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

enclosure = EnclosureManager(screen)

grass = pygame.image.load('resources/grass4.png').convert()
grass = pygame.transform.scale(grass, (int(config.TILE_SIZE), int(config.TILE_SIZE)))

chicken = pygame.image.load('resources/chicken.png').convert_alpha()
chicken = pygame.transform.scale(chicken, (int(config.TILE_SIZE), int(config.TILE_SIZE)))

pygame.display.set_icon(chicken)
pygame.display.set_caption("ZooTrophic")

# -------------------------- MAIN LOOP -------------------------------- #

while running:

    dt = clock.tick(60) / 1000

    for event in pygame.event.get():

        enclosure.handle_event(event)

        if event.type == pygame.QUIT:
            running = False

    #screen.fill("darkolivegreen2")
    #pygame.draw.circle(screen, "red", (xpos,400), 40, 5)

    tile = pygame.Rect(0, 0, config.TILE_SIZE, config.TILE_SIZE)

    for y in range(0, int(config.SCREENHEIGHT), int(config.TILE_SIZE)):
        for x in range(0, int(config.SCREENWIDTH), int(config.TILE_SIZE)):
            color = "darkolivegreen2"

            # if x > (config.SCREENWIDTH / 2):
            #     color = "red"
            # else:
            #     color = "darkolivegreen2"

            tile.left = x
            screen.blit(grass, (x, y))
            
        tile.top = y
        tile.left = 0

    # for x in range(0, int(config.SCREENWIDTH), int(config.TILE_SIZE)):
    #     pygame.draw.line(screen, "black", (x, 0), (x, config.SCREENHEIGHT))

    # for y in range(0, int(config.SCREENHEIGHT), int(config.TILE_SIZE)):
    #     pygame.draw.line(screen, "black", (0, y), (config.SCREENWIDTH, y))


    mousepos = pygame.mouse.get_pos()

    enclosure.update(((mousepos[0] // config.TILE_SIZE), (mousepos[1] // config.TILE_SIZE)), dt)
    enclosure.draw_enclosures(dt)

    screen.blit(chicken, (100, 100))
    
    pygame.display.flip()

pygame.quit()