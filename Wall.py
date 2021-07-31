import pygame
from constants import *

class Wall(pygame.sprite.Sprite):

    def __init__(self, hard, row, column, image):
        super(Wall, self).__init__()
        self.hard = hard
        self.image = image
        self.rect = self.image.get_rect()
        self.row = row
        self.column = column
        self.rect.x = self.column * BLOCK_SIZE
        self.rect.y = self.row * BLOCK_SIZE





