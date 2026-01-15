import pygame
import config
from gamestate import GameManager

# Setup
pygame.init()
screen = pygame.display.set_mode((config.SCREENWIDTH,config.SCREENHEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True
dt = 0

gameManager = GameManager(screen)

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

        gameManager.handle_event(event)

        if event.type == pygame.QUIT:
            running = False

    tile = pygame.Rect(0, 0, config.TILE_SIZE, config.TILE_SIZE)

    for y in range(0, int(config.SCREENHEIGHT), int(config.TILE_SIZE)):
        for x in range(0, int(config.SCREENWIDTH), int(config.TILE_SIZE)):
            color = "darkolivegreen2"

            tile.left = x
            screen.blit(grass, (x, y))
            
        tile.top = y
        tile.left = 0

    mousepos = pygame.mouse.get_pos()

    gameManager.update(dt, mousepos)
    gameManager.draw(dt)

    screen.blit(chicken, (100, 100))
    
    pygame.display.flip()

pygame.quit()