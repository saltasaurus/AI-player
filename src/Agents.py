'''The Agent class and all subclasses

Specific agents are created using the Agent Superclass
'''

from src.constants import red_agent

import abc
import pygame as pg
import math


class Agent():
    '''Base class for all agent actions
    
    New agents must define Heuristic function: get_target( )'''

    step = 10

    def __init__(self, initial_x, initial_y):
        self.r_img = red_agent
        self.l_img = pg.transform.flip(red_agent, True, False)
        self.surface = None
        self.x = initial_x
        self.y = initial_y
        self.score = 0
        self.targetCoin = None
        self.type = None

    def update(self):
        pass

    def show_score(self):
        pass

    def target(self):
        pass

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))

    def __str__(self):
        return f'This agent is a {self.type}'

    # @abc.abstractmethod
    def setTarget(self):
        '''Set agents next target'''
        pass

