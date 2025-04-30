#Game Template

import pygame
from pygame import gfxdraw
pygame.init()
import random
import math
import time



def main():
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


    BACKGROUND_COLOR = (black)
    clock = pygame.time.Clock()

    delta_time = 1/fps

    playing = True
    while playing:
        start = time.time()

        handle_events(pygame.event.get())

        game_tick(delta_time)

        game_draw(window)

        pygame.display.flip()
        if fps > 0:
            clock.tick(fps)
        delta_time = time.time()-start

    pygame.quit()

def handle_events(events):
    for event in events:
        if event.type == pygame.QUIT:
            playing = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                playing = False
                break

def game_draw(surface):
    surface.fill(0, 0, 0)

def game_tick(delta_time):
    pass

main()