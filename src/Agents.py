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
        self.actions = []
        self.hitbox = pg.Rect(self.x+4, self.y+4, 28, 28)

    def update(self):
        '''Update agent based on action taken'''

        for action in self.actions:
            if action == 'right':
                self.moveRight()
                break
            elif action == 'left':
                self.moveLeft()
                break
            elif action == 'up':
                self.moveUp()
                break
            elif action == 'down':
                self.moveDown()
                break
        else:
            pass


    def moveLeft(self):
        '''Sets action when moving left'''
        self.x = self.x - self.step
        self.hitbox.left -= self.step
        if self.l_img is not None:
            self._surface = self.l_img.convert_alpha()

    def moveRight(self):
        '''Sets action when moving right'''
        self.x = self.x + self.step
        self.hitbox.left += self.step
        if self.r_img is not None:
            self._surface = self.r_img.convert_alpha()

    def moveUp(self):
        '''Sets action when moving up'''
        self.y = self.y - self.step
        self.hitbox.top -= self.step
        if self.up_img is not None:
            self._surface = self.up_img

    def moveDown(self):
        '''Sets action when moving down'''
        self.y = self.y + self.step
        self.hitbox.top += self.step
        if self.down_img is not None:
            self._surface = self.down_img

    def check_agent_collision(self, hitbox, agent_hitbox):
        '''Determine if moved hitbox collides with another agent's hitbox'''
        if pg.Rect.colliderect(hitbox, agent_hitbox):
            return True
        else:
            return False

    # BUG -> Still collide and overlap
    def get_moves(self, agents):
        move_left = pg.Rect.move(self.hitbox, (-1 * self.step, 0))
        move_right = pg.Rect.move(self.hitbox, (self.step, 0))
        move_up = pg.Rect.move(self.hitbox, (0, -1 * self.step))
        move_down = pg.Rect.move(self.hitbox, (0, self.step))
        
        for agent in agents:
            if agent != self:
                hb = agent.hitbox
                for action in self.actions:
                    if action == 'left' and self.check_agent_collision(move_left, hb):
                        self.actions.remove('left')
                    elif action == 'right' and self.check_agent_collision(move_right, hb):
                        self.actions.remove('right')
                    elif action == 'up' and self.check_agent_collision(move_up, hb):
                        self.actions.remove('up')
                    elif action == 'down' and self.check_agent_collision(move_down, hb):
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
        
        return pg.Rect.colliderect(self.hitbox, coin.hitbox)

    def distanceToCoin(self, coin: object) -> float:
        '''Calculate distance between Agent and a Coin'''
        return (((self.x - coin.x) ** 2 + (self.y - coin.y) ** 2) ** .5) / 10

    def show_score(self, surface, choice, width, color, font):

            score_surf = font.render(self.type + "'s Score: " + str(self.score), True, color)
            score_rect = score_surf.get_rect()

            
            score_rect.midtop = (width - width/10, 15*choice)
            
            surface.blit(score_surf, score_rect)

    def draw(self, surface, image):
        # pg.draw.rect(surface, (0, 0, 0), self.hitbox, 1)
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