'''The Agent class and all subclasses

Specific agents are created using the Agent Superclass
'''

from src.constants import red_agent, penguin_agent

import abc
import pygame as pg


class Agent():
    '''Base class for all agent actions
    
    New agents must define Heuristic function: get_target( )'''

    step = 2

    def __init__(self, agent_type, initial_x, initial_y):
        # self.r_img = red_agent
        # self.l_img = pg.transform.flip(red_agent, True, False)
        self.l_img = penguin_agent
        self.r_img = pg.transform.flip(penguin_agent, True, False)
        self.surface = None
        self.x = initial_x
        self.y = initial_y
        self.score = 0
        self.targetCoin = None
        self.type = agent_type
        self.action = None
        # self.moves_list = set()

    def update(self):
        '''Update agent based on action taken'''
        if self.action in self.moves_list:
            if self.action == 'right':
                self.x = self.x + self.step
            elif self.action == 'left':
                self.x = self.x - self.step
            elif self.action == 'up':
                self.y = self.y - self.step
            elif self.action == 'down':
                self.y = self.y + self.step
        else:
            print("standing still")

    def moveLeft(self):
        '''Sets action when moving left'''
        self.action = 'left'
        self._surface = self.l_img.convert_alpha()

    def moveRight(self):
        '''Sets action when moving right'''
        self.action = 'right'
        self._surface = self.r_img.convert_alpha()

    def moveUp(self):
        '''Sets action when moving up'''
        self.action = 'up'

    def moveDown(self):
        '''Sets action when moving down'''
        self.action = 'down'

    def show_score(self):
        pass

    # BUG -> Still collide and overlap
    def get_moves(self, agents):
        self.moves_list = set()
        for agent in agents:
            if ((self.x + self.step) != agent.x):
                self.moves_list.add('right')
            if ((self.x - self.step) != agent.x):
                self.moves_list.add('left')
            if ((self.y + self.step) != agent.y):
                self.moves_list.add('down')
            if ((self.y - self.step) != agent.y):
                self.moves_list.add('up')

    def target(self):
        tx = self.targetCoin.x
        ty = self.targetCoin.y

        if self.x > tx:
            self.moveLeft()

        elif self.x < tx:
            self.moveRight()
        else:
            if self.y < ty:
                self.moveDown()
            elif self.y > ty:
                self.moveUp()

    def distanceToCoin(self, coin: object) -> float:
        '''Calculate distance between Agent and a Coin'''
        return (((self.x - coin.x) ** 2 + (self.y - coin.y) ** 2) ** .5) / 10

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))

    def __str__(self):
        return f'This agent is {self.type}'

    @abc.abstractmethod
    def setTarget(self):
        '''Set agents next target'''
        pass


class ClosestCoinAgent(Agent):

    def __init__(self, x, y, initial_coins):
        super().__init__("ClosestCoin", x, y)
        # TODO
        # Give new images > Use base images for now
        # self.r_img = None
        # self.l_img = None
        self._surface = None
        self.setTarget(initial_coins)

    def setTarget(self, coins):
        self.targetCoin = self.getClosestCoin(coins)

    def getClosestCoin(self, coins):
        '''Algorithm'''
        closestCoin = coins[0]
        smallestDistance = self.distanceToCoin(closestCoin)

        for coin in coins:
            dist = self.distanceToCoin(coin)
            if dist < smallestDistance:
                smallestDistance = dist
                closestCoin = coin

        if coin:
            return closestCoin
        else:
            raise ValueError