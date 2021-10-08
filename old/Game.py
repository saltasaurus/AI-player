from src.Board import Board
from src.Agents import ClosestCoinAgent, Djikstra, Greedy, GreedyClose
from src.Items import Coin
import pygame as pg
from pygame.locals import *
import random
import numpy as np
  
# Colors
# TODO Add to file for other color manage (i.e. colorblind mode)
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)


class Game():
    '''Defines the rules for the Agents
    and handles all interactions'''

    def __init__(self, width, height, names):
        '''
        :param width: (int) Width of Game window
        :param height: (int) Height of Game window
        :param agents: ([string]) List of agent types
        '''
        self.WIDTH = width
        self.HEIGHT = height
        self.names = names
        self.TOTAL_ROUNDS = 1
        self._FPS = 60
        

        self._running = None

    def on_init(self):
        '''Reset game'''
        # Initialize pygame
        pg.init()
        # self.font = pg.font.SysFont('consalas', 20)

        self._running = True

        self.clock = pg.time.Clock()
        self.clock_tick = self.clock.tick(self._FPS)

        self.init_pos = []
        self.create_board()
        self.create_coins(50)
        self.create_agents()
        del self.init_pos

        # Initialize window
        self.board.set_window()
        
        # initialize surfaces
        self.board.set_surfaces(self.agents)

    # Functions that initialize the board, coins and agents
    def create_board(self):
        self.board = Board(self.WIDTH, self.HEIGHT)

    def create_coins(self, n=30):
        self.coins = []
        
        for i in range(n):
            x = random.randrange(0, self.WIDTH-20, 2)
            y = random.randrange(0, self.HEIGHT-20, 2)

            value = random.randint(1, 7)

            coin = Coin(x, y, value, i)
            self.coins.append(coin)
        
                
    def create_agents(self):
        self.agents = []
        spacing = self.HEIGHT // len(self.names)

        self.agentTypes = ["Closest", "Djikstra", "GreedyClose"]


        for i, name in enumerate(self.names):
            new_agent = None
            x = 10
            y = spacing * i

            if y > self.HEIGHT-40:
                break
            
            print(name)

            if self.agentTypes[i] == 'Closest':
                new_agent = ClosestCoinAgent(x=x, y=y, initial_coins=self.coins)
            elif self.agentTypes[i] == 'Djikstra':
                new_agent = Djikstra(x=x, y=y, initial_coins=self.coins)
            elif self.agentTypes[i] == 'Greedy':
                new_agent = Greedy(x=x, y=y, initial_coins=self.coins)
            elif self.agentTypes[i] == 'GreedyClose':
                new_agent = GreedyClose(x, y, self.coins)

            if new_agent is not None:
                new_agent.name = name
                self.agents.append(new_agent)
            else:
                raise ValueError


    # Functions that handle events
    def on_play(self):
        '''Begins game!'''
        self._run()


    def on_event(self, event):
        '''Quit game if X (exit) is pressed'''
        if event.type == QUIT:
            self._running = False

    def on_cleanup(self):
        '''Close PyGame window'''
        pg.quit()

    # Functions that handle gameplay
    def on_loop(self):
        for agent in self.agents:
            #agent.setTarget(self.coins)
            if agent.targetCoin not in self.coins:
                agent.get_new_target = True
                continue


            agent.target()
            agent.get_moves(self.agents)
            agent.update()

            for coin in self.coins:
                if agent.collect_coin(coin):
                    agent.score += coin.value
                    if coin == agent.targetCoin:
                        agent.get_new_target = True
                    self.coins.remove(coin)
                    if len(self.coins) == 0:
                        self._running = False
                        return
                
        for agent in self.agents:
            if agent.get_new_target:
                agent.setTarget(self.coins)
                agent.get_new_target = False

    def on_render(self):
        '''Calls board object to render game'''
        self.board.render(self.coins, self.agents)

    def get_winner(self):
        print("Final Scores: ")
        winner = None
        winner_score = -1
        for agent in self.agents:
            print(f'{(agent.name)} | Score: {str(agent.score)}')
            if agent.score > winner_score:
                winner = agent
                winner_score = agent.score
        # log winner and rest of the scores
        print(f'({winner.name}) wins with a score of {str(winner.score)}!')
    
    def _run(self):
        
        # Check for init failure
        if self.on_init() == False:
            self._running = False


        
        # Main game loop
        while self._running:
            self.clock.tick(self._FPS)
            # Check if user quits
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self._running = False
            pg.event.pump()
            self.on_loop()
            self.on_render()

        # Actions after game ends
        self.get_winner()

        self.on_cleanup()
        
        

    def __str__(self) -> str:
        return f'Game dimensions: {self.WIDTH} x {self.HEIGHT}'
    

