import pygame
import sys
from constantes import *

class Widget:
    def __init__(self, master_surface, x, y, w, h, color_back, color_border):
        self.master_surface = master_surface
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color_back = color_back
        self.color_border = color_border

    def render(self):
        pass

    def update(self):
        pass

    def draw(self, master_surface):
        master_surface.blit(self.slave_surface, self.slave_rect)
 

