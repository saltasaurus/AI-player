from src.Board import Board
from src.Agents import ClosestCoinAgent
from src.Items import Coin
import pygame as pg
from pygame.locals import *
import random

# Colors
# TODO Add to file for other color manage (i.e. colorblind mode)
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)


class Game():
    '''Defines the rules for the Agents
    and handles all interactions'''

    def __init__(self, width, height, agents):
        '''
        :param width: (int) Width of Game window
        :param height: (int) Height of Game window
        :param agents: ([string]) List of agent types
        '''
        self.WIDTH = width
        self.HEIGHT = height
        self.agentTypes = agents
        self.coins = []
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
        self.create_board(self.WIDTH, self.HEIGHT)
        self.create_coins(100)
        self.create_agents()
        del self.init_pos

        # Initialize window
        self.board.set_window()
        
        # initialize surfaces
        self.board.set_surfaces(self.agents)

    # Functions that initialize the board, coins and agents
    def create_board(self, width, height):
        self.board = Board(width, height)

    def create_coins(self, n: int):
        '''Initialize all collectables' positions
        
        :param n: Number of collectables to create'''
        
        for _ in range(n):
            while(True):
                x = random.randrange(0, self.WIDTH, 40)
                y = random.randrange(0, self.HEIGHT, 40)
                pos = f'{x},{y}'
                if pos not in self.init_pos:
                    break

            self.init_pos.append(pos)
            self.coins.append(Coin(x,y,1))

    def create_agents(self):
        self.agents = {}

        # Loop through all agents
        for agent in self.agentTypes:
            while(True):
                # Find untaken location and set as key
                x = random.randrange(0, self.WIDTH, 40)
                y = random.randrange(0, self.HEIGHT, 40)
                key = f'{x},{y}'
                if key not in self.init_pos:
                    break
    
            self.agents[key] = ClosestCoinAgent(x=x, y=y, initial_coins=self.coins)
            self.agents[key].type = agent
        

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
        for agent in self.agents.values():
            agent.setTarget(self.coins)
            agent.target()
            agent.get_moves(self.agents.values())
            agent.update()

            for coin in self.coins:
                get_new_target = False
                if agent.collect_coin(coin):
                    agent.score += coin.value
                    if coin == agent.targetCoin:
                        get_new_target = True
                    if coin in self.coins:
                        self.coins.remove(coin)
                        if len(self.coins) == 0:
                            self._running = False
                            return
                    # Set agent's next target
                    if get_new_target:
                        agent.setTarget(self.coins)

    def on_render(self):
        '''Calls board object to render game'''
        self.board.render(self.coins, self.agents)

    def get_winner(self):
        print("Final Scores: ")
        winner = None
        winner_score = -1
        for _, agent in self.agents.items():
            print(f'{(agent.type)} | Score: {str(agent.score)}')
            if agent.score > winner_score:
                winner = agent
                winner_score = agent.score
        # log winner and rest of the scores
        print(f'({winner.type}) wins with a score of {str(winner.score)}!')

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

    
        


