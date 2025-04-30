#Game Template
from world import World
from actor import Actor

import pygame
from pygame import gfxdraw
pygame.init()
import random
import math






def main():
    myWorld = World()

    width, height = 1280, 720
    fps = 60

    window = pygame.display.set_mode([width, height])
    pygame.display.set_caption("Placeholder")

    white = (255, 255, 255)
    light_gray = (192, 192, 192)
    gray = (128, 128, 128)
    dark_gray = (64, 64, 64)
    black = (0, 0, 0)

    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

    BACKGROUND_COLOR = black
    clock = pygame.time.Clock()

    playing = True
    while playing:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    playing = False
                    break


        window.fill(BACKGROUND_COLOR)


        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

main()