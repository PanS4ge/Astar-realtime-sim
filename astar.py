import time
import pygame
import pyastar2d
import numpy as np
import math

def request_path(startpixel, endpixel, walls, pixelsize):
    try:
        start, end, maze = translate_to_maze(startpixel, endpixel, walls, pixelsize)
        at = pyastar2d.astar_path(np.array(maze, dtype=np.float32), start, end, True)
        if not(isinstance(at, np.ndarray)): return []
        return at
    except:
        return []

def translate_to_maze(startpixel, endpixel, walls, pixelsize):
    square_wall = int(800 / pixelsize)
    w = []
    for x in range(square_wall):
        curr = []
        for y in range(square_wall):
            curr.append(1)
        w.append(curr)
    for x in walls:
        w[int(x[0] / pixelsize)][int(x[1] / pixelsize)] = math.inf
    start = (int(startpixel[0] / pixelsize), int(startpixel[1] / pixelsize))
    end = (int(endpixel[0] / pixelsize), int(endpixel[1] / pixelsize))
    return (start, end, w)