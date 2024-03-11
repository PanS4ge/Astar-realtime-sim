import pygame
import time
import math
from . import astar
import numpy as np

pressed = []
pygame.init()

screen = pygame.display.set_mode([800, 800])

CELLSIZE = 25
SQUARESIZE = 5

lastdrawn = time.time()

status = 0 # 0 - begin 1 - end
pixelbegin = (0, 0)
pixelend = (800 - CELLSIZE, 800 - CELLSIZE)

deletemode = False

running = True

justgened = False

lastdrawn = time.time()

arr = []
arrbak = []

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

def are_arrays_the_same(arr1 : np.ndarray, arr2 : np.ndarray):
    if(len(arr1) != len(arr2)):
        return False
    for x in range(len(arr1)):
        if(arr1.ravel()[x] != arr2.ravel()[x]):
            return False
    return True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    color = (255,255,255)

    for x in range(CELLSIZE, 800, CELLSIZE):
        pygame.draw.rect(screen, color, pygame.Rect(x, 0, 1, 800))
        pygame.draw.rect(screen, color, pygame.Rect(0, x, 800, 1))
        
    for pixel in pressed:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(pixel[0], pixel[1], CELLSIZE, CELLSIZE))

    arrbak = astar.request_path(pixelbegin, pixelend, pressed, CELLSIZE)
    if(len(arrbak) != 0):
        arr = arrbak
    
    for event in pygame.event.get():
        # handle MOUSEBUTTONUP
        if event.type == pygame.MOUSEMOTION:
            if(pygame.mouse.get_pressed()[0] == True):
                pos = pygame.mouse.get_pos()
                pixel = (math.floor(pos[0] / CELLSIZE) * CELLSIZE, math.floor(pos[1] / CELLSIZE) * CELLSIZE)
                if pixel in pressed and deletemode:
                    pressed.remove(pixel)
                if not pixel in pressed and not deletemode:
                    pressed.append(pixel)
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            if(pygame.mouse.get_pressed()[1]):
                deletemode = not deletemode
            elif(pygame.mouse.get_pressed()[2]):
                pos = pygame.mouse.get_pos()
                status = status % 2
                status += 1
                if(status == 1):
                    pixelbegin = (math.floor(pos[0] / CELLSIZE) * CELLSIZE, math.floor(pos[1] / CELLSIZE) * CELLSIZE)
                else:
                    pixelend = (math.floor(pos[0] / CELLSIZE) * CELLSIZE, math.floor(pos[1] / CELLSIZE) * CELLSIZE)
            else:
                pos = pygame.mouse.get_pos()
                pixel = (math.floor(pos[0] / CELLSIZE) * CELLSIZE, math.floor(pos[1] / CELLSIZE) * CELLSIZE)
                if pixel in pressed:
                    pressed.remove(pixel)
                else:
                    pressed.append(pixel)
            lastdrawn = time.time()

    for x in arr:
        pygame.draw.rect(screen, (0, 255, 0) if are_arrays_the_same(arr, arrbak) else (0, 122, 0), pygame.Rect(x[0] * CELLSIZE, x[1] * CELLSIZE, CELLSIZE, CELLSIZE))

    for pixel in pressed:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(pixel[0], pixel[1], CELLSIZE, CELLSIZE))
    
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(pixelbegin[0], pixelbegin[1], CELLSIZE, CELLSIZE))
    pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(pixelend[0], pixelend[1], CELLSIZE, CELLSIZE))

    pygame.display.flip()
pygame.quit()