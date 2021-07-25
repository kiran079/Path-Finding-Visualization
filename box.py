import pygame
from colors import *

num_to_color = {0: GREEN, 1: RED, 2: GRAY, 3: WHITE, 4: PURPLE, 5: YELLOW, 6: LIME}

class Box:
    def __init__(self,window, x , y, length):
        self.window = window
        self.color = WHITE
        self.type = 3
        self.rect = pygame.Rect(x, y, length, length)

    def __eq__(self, other):
        return (self.rect.center == other.rect.center)

    def setColor(self, color):
        self.color = color

    def draw(self):
        pygame.draw.rect(self.window, self.color, self.rect)
        pygame.draw.rect(self.window, BLACK, self.rect, width=1, border_radius=2)

    def getCollision(self, pos):
        return self.rect.collidepoint(pos)

    def setType(self, num):
        self.type = num
        self.color = num_to_color[num]


    