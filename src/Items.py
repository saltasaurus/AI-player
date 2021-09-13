'''Item classes

Coins'''

from src.constants import coin_img
import pygame as pg
from pygame.locals import *

class Coin():
    '''Collectable object worth points'''

    def __init__(self, x, y, value):
        '''
        :param x: (int) Horizontal location of the coin
        :param y: (int) Vertical location of the coin
        :param value: (int) Points the coin is worth
        '''
        self.img = coin_img
        self._surface = None
        self.x = x
        self.y = y
        self.value = value
    
    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))
