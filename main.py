#!/usr/bin/python3
import pygame
from settings import screen_height,tile_size,screen_width
from game_data import levels
from level import Level
#from temp3 import Level
pygame.init()

window = pygame.display.set_mode((screen_width,screen_height))
def main():
    run = True 
    clock = pygame.time.Clock()
    level = Level(levels,window)
    #print(dir(pygame.sprite))
    while run:
        clock.tick(40)
        window.fill('black')
        level.run()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                        run = False
main()
    
