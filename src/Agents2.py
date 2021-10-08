'''The Agent class and all subclasses

Specific agents are created using the Agent Superclass
'''
from src.Items import Coin
from src.constants import *

import abc
import pygame as pg


class Agent:
    '''Base class for all agent actions
    
    New agents must define Heuristic function: get_target( )'''

    step = 2

    def __init__(self, agent_type, start=(50, 300), end=(750, 300)):
        self.r_img = red_agent
        self.l_img = pg.transform.flip(red_agent, True, False)
        self.up_img = None
        self.down_img = None
        self.surface = None
        self.x = start[0]
        self.y = start[1]
        self.end_point = Coin(end[0], end[1], 0, -1)
        self.score = 0
        self.targetCoin = None
        self.type = agent_type
        self.name = None
        self.actions = []
        self.get_new_target = False
        self.path = []
        self._path = []
        self.current_coin = 0

    def update(self):
        '''Update agent based on action taken'''
        # print(self.name, self.actions)
        for action in self.actions:
            if action == 'right':
                self.moveRight()
            elif action == 'left':
                self.moveLeft()
            elif action == 'up':
                self.moveUp()
            elif action == 'down':
                self.moveDown()

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

    
    def next_coin_index(self):
        self.current_coin += 1

    def collect_coin(self, coin):
        collect = self.x == coin.x and self.y == coin.y
        if collect:
            self.next_coin_index()
            self.setTarget()

        return collect

    def show_score(self, surface, choice, width, color, font):

            score_surf = font.render(self.name + "'s Score: " + str(self.score), True, color)
            score_rect = score_surf.get_rect()

            score_rect.midtop = (width - width/10, 15*choice)
            
            surface.blit(score_surf, score_rect)

    def draw(self, surface, image):
        hitbox = pg.Rect(self.x-16, self.y-16, 32, 32)
        pg.draw.rect(surface, (0, 0, 0), hitbox, 1)
        pg.draw.line(surface, (0, 0, 0), (self.x, self.y), (self.targetCoin.x, self.targetCoin.y))
        for i in range(1,len(self.path)):
            s = self.path[i-1]
            t = self.path[i]
            pg.draw.line(surface, (0,0,0), (s.x, s.y), (t.x, t.y))
        surface.blit(image, (self.x-16, self.y-16))
    
    def Agent2Coin(self, coin: object) -> float:
        '''Calculate distance between Agent and a Coin'''
        return (((self.x - coin.x) ** 2 + (self.y - coin.y) ** 2) ** .5) / 10

    def Coin2Coin(self, coin1, coin2):
            '''Distance between two coins'''
            return (((coin1.x - coin2.x) ** 2 + (coin1.y - coin2.y) ** 2) ** .5) / 10

    def __str__(self):
        return f'This agent is {self.type}'

    @abc.abstractmethod
    def setTarget(self):
        '''Set agents next target'''
        pass

    def create_path(self, coins):
        pass


class ClosestCoinAgent(Agent):

    def __init__(self, x, y, initial_coins):
        super().__init__("ClosestCoin", (x, y))
        # TODO
        # Give new images > Use base images for now
        # self.r_img = None
        # self.l_img = None
        self._surface = None
        self.MAX_COINS = len(initial_coins)
        self.create_path(initial_coins)
        self.setTarget()
        # In super
        # self.path = []
        # self.current_coin = 0

    def setTarget(self):
        if self.current_coin >= self.MAX_COINS:
            return
        self.targetCoin = self.path[self.current_coin]

    def create_path(self, coins):

        all_coins = {}
        for coin in coins:
            all_coins[coin.id] = coin

        unvisited = {coin.id:(coin.x, coin.y) for coin in coins}

        # Gets first coin (closest to agent)
        first_coin_dist = 1e5
        first_coin_id = None
        for id, _ in unvisited.items():
            coin = all_coins[id]
            dist = self.distance(self.x, self.y, coin.x, coin.y)
            if dist < first_coin_dist:
                first_coin_dist = dist
                first_coin_id = id

        # Get first coin in path
        first_coin = all_coins[first_coin_id]

        # Attach it to Agent's path
        self.path.append(first_coin)

        # Save coins position
        prev_x = first_coin.x
        prev_y = first_coin.y

        # Remove from possible moves
        unvisited.pop(first_coin_id)


        # Gets next closest coin from the previous 
        # Breaks once all coins are collected
        while unvisited != {}:
            # Reset best coin
            lowest_dist = 1e5
            best_id = None

            # Find best coin based on distance only
            for id, pos in unvisited.items():
                coin = all_coins[id]
                dist = self.distance(prev_x, prev_y, pos[0], pos[1]) 
                if dist < lowest_dist:
                    lowest_dist = dist
                    best_id = id

            # Leave if closest coin is the end
            if first_coin_id == -1:
                self.path.append(self.end_point)
                return

            # Get closest coin from ID
            next_coin = all_coins[best_id]
            # Add coin to Agent's path
            self.path.append(all_coins[best_id])

            # Reset current pos as chosen coin's
            prev_x = next_coin.x
            prev_y = next_coin.y

            # Remove coin from possible moves
            unvisited.pop(best_id)

    def distance(self, ob1x, ob1y, ob2x, ob2y):
        return (((ob1x - ob2x) ** 2 + (ob1y - ob2y) ** 2) ** .5) / 10


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

    
