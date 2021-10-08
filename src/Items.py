'''Item classes

Coins'''

from src.constants import coin_img, colors
import pygame as pg

class Coin():
    '''Collectable object worth points'''

    def __init__(self, x, y, value, id=None):
        '''
        :param x: (int) Horizontal location of the coin
        :param y: (int) Vertical location of the coin
        :param value: (int) Points the coin is worth
        :param id: (int) Unique ID of coin 
        '''
        # self.img = coin_img
        self.img = coin_img
        self._surface = None
        self.x = x
        self.y = y
        self.value = value
        self.id = id
        self.end_point = False

        self.set_constants()
    
    def set_constants(self):
        if self.id == -1:
            self.color = colors["RED"]
            self.end_point = True
        else:
            self.color = colors["BLACK"]
    
    def draw(self, surface):
        if self.end_point:
            pg.draw.rect(surface, self.color, (self.x-10, self.y-10, 20, 20))
        else:
            pg.draw.rect(surface, self.color, (self.x-10, self.y-10, 20, 20), 1)
        surface.blit(self.img, (self.x-10, self.y-10))

    def __str__(self):
        return f'{self.id}'
