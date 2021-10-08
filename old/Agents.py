'''The Agent class and all subclasses

Specific agents are created using the Agent Superclass
'''

from src.constants import *

import abc
import pygame as pg


class Agent:
    '''Base class for all agent actions
    
    New agents must define Heuristic function: get_target( )'''

    step = 2

    def __init__(self, agent_type, initial_x, initial_y):
        self.r_img = red_agent
        self.l_img = pg.transform.flip(red_agent, True, False)
        self.up_img = None
        self.down_img = None
        self.surface = None
        self.x = initial_x
        self.y = initial_y
        self.score = 0
        self.targetCoin = None
        self.type = agent_type
        self.name = None
        self.actions = []
        self.get_new_target = False

    def update(self):
        '''Update agent based on action taken'''
        # print(self.name, self.actions)
        for action in self.actions:
            if action == 'right':
                self.moveRight()
                #break
            elif action == 'left':
                self.moveLeft()
                #break
            elif action == 'up':
                self.moveUp()
                #break
            elif action == 'down':
                self.moveDown()
                #break
        else:
            pass


    def moveLeft(self):
        '''Sets action when moving left'''
        self.x = self.x - self.step
        if self.l_img is not None:
            self._surface = self.l_img.convert_alpha()

    def moveRight(self):
        '''Sets action when moving right'''
        self.x = self.x + self.step
        if self.r_img is not None:
            self._surface = self.r_img.convert_alpha()

    def moveUp(self):
        '''Sets action when moving up'''
        self.y = self.y - self.step
        if self.up_img is not None:
            self._surface = self.up_img

    def moveDown(self):
        '''Sets action when moving down'''
        self.y = self.y + self.step
        if self.down_img is not None:
            self._surface = self.down_img

    def check_agent_collision(self, move, agent):
        '''Determine if moved hitbox collides with another agent's hitbox'''
        # return False
        if move == (agent.x, agent.y):
            return True
        else:
            return False

    def get_moves(self, agents):
        move_left = (self.x - self.step, self.y)
        move_right = (self.x + self.step, self.y)
        move_up = (self.x, self.y  - self.step)
        move_down = (self.x, self.y + self.step)
        
        for agent in agents:
            if agent != self:
                for action in self.actions:
                    if action == 'left' and self.check_agent_collision(move_left, agent):
                        self.actions.remove('left')
                    elif action == 'right' and self.check_agent_collision(move_right, agent):
                        self.actions.remove('right')
                    elif action == 'up' and self.check_agent_collision(move_up, agent):
                        self.actions.remove('up')
                    elif action == 'down' and self.check_agent_collision(move_down, agent):
                        self.actions.remove('down')

    def target(self):
        tx = self.targetCoin.x
        ty = self.targetCoin.y
        self.actions = []

        if self.x > tx:     # Left
            self.actions.append('left')

        elif self.x < tx:   # Right
            self.actions.append('right')
        
        if self.y < ty:     # Down
            self.actions.append('down')

        elif self.y > ty:   # Up
            self.actions.append('up')


    def collect_coin(self, coin):
        
        return (self.x == coin.x and self.y == coin.y)

    def Agent2Coin(self, coin: object) -> float:
        '''Calculate distance between Agent and a Coin'''
        return (((self.x - coin.x) ** 2 + (self.y - coin.y) ** 2) ** .5) / 10

    def show_score(self, surface, choice, width, color, font):

            score_surf = font.render(self.name + "'s Score: " + str(self.score), True, color)
            score_rect = score_surf.get_rect()

            score_rect.midtop = (width - width/10, 15*choice)
            
            surface.blit(score_surf, score_rect)

    def draw(self, surface, image):
        hitbox = pg.Rect(self.x-16, self.y-16, 32, 32)
        pg.draw.rect(surface, (0, 0, 0), hitbox, 1)
        pg.draw.line(surface, (0, 0, 0), (self.x, self.y), (self.targetCoin.x, self.targetCoin.y))
        surface.blit(image, (self.x-16, self.y-16))
    
    def Coin2Coin(self, coin1, coin2):
            '''Distance between two coins'''
            return (((coin1.x - coin2.x) ** 2 + (coin1.y - coin2.y) ** 2) ** .5) / 10

    def __str__(self):
        return f'This agent is {self.type}'

    @abc.abstractmethod
    def setTarget(self):
        '''Set agents next target'''
        pass

    def create_path(self, pos):
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

    def setTarget(self, coins: list):
        self.targetCoin = self.getClosestCoin(coins)

    def getClosestCoin(self, coins):
        '''Algorithm'''
        closestCoin = coins[0]
        smallestDistance = self.Agent2Coin(closestCoin)

        for coin in coins:
            dist = self.Agent2Coin(coin)
            if dist < smallestDistance:
                smallestDistance = dist
                closestCoin = coin

        if coin:
            return closestCoin
        else:
            raise ValueError

class GreedyClose(Agent):
    def __init__(self, x, y, initial_coins):
        super().__init__('GreedyClose', x, y)

        self._surface = None
        self.setTarget(initial_coins)

    def setTarget(self, coins):
        self.targetCoin = self.algorithm(coins)

    def algorithm(self, coins):
        # Searches for closest, most valuable coin
        BestCoin = coins[0]
        best = BestCoin.value / ( self.Agent2Coin(coins[0]) / 100)

        for coin in coins:
            value = BestCoin.value / ( self.Agent2Coin(coin) / 100)
            if value > best:
                best = value
                BestCoin = coin

        return BestCoin

class Greedy(Agent):

    def __init__(self, x, y, initial_coins):
        super().__init__('Greedy', x, y)

        self._surface = None
        self.setTarget(initial_coins)

    def setTarget(self, coins):
        self.targetCoin = self.greedy(coins)

    def greedy(self, coins):
        BestCoin = coins[0]
        value = BestCoin.value

        for coin in coins:
            dist = coin.value
            if dist == value:
                if self.Agent2Coin(BestCoin) > self.Agent2Coin(coin):
                    value = dist
                    BestCoin = coin
            elif dist > value:
                value = dist
                BestCoin = coin

        return BestCoin

class Djikstra(Agent):

    def __init__(self, x, y, initial_coins):
        super().__init__('Djikstra', x, y)

        self._surface = None
        self.setTarget(initial_coins)

    def setTarget(self, coins):
        self.targetCoin = self.djikstra(coins)

    def djikstra(self, coins):
        BestCoin = coins[0]
        value = self.Agent2Coin(BestCoin) * BestCoin.value

        for coin in coins:
            dist = self.Agent2Coin(coin) * coin.value
            if dist > value:
                value = dist
                BestCoin = coin

        if coin:
            return BestCoin
        else:
            raise ValueError

    
