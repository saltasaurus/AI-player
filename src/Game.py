from src.Board import Board
from src.Agents import Agent
from src.Items import Coin
from src.constants import coin_img
import pygame as pg
from pygame.locals import *
import time
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

        self._running = None

        # Display
        self._display_surf = None

    def on_init(self):
        '''Reset game'''
        # Initialize pygame
        pg.init()
        self.font = pg.font.SysFont('consalas', 20)
        self._running = True

        self.create_board(self.WIDTH, self.HEIGHT)
        self.create_coins(100)
        self.create_agents()
        del self.init_pos

        # Initialize window
        pg.display.set_caption("AI Coliseum")
        self._display_surf = pg.display.set_mode((self.WIDTH, self.HEIGHT), pg.HWSURFACE)
        
        # initialize surfaces
        self._coin_surface = coin_img.convert()
        for _, agent in self.agents.items():
            agent._surface = agent.r_img.convert_alpha()


    # Functions that initialize the board, coins and agents
    def create_board(self, width, height):
        self.board = Board(width, height)

    def create_coins(self, n: int):
        # BUG
        self.init_pos = []
        
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
        # BUG
        self.agents = {}

        for agent in self.agentTypes:
            # Loop through all agents
            while(True):
                # Find untaken location and set as key
                x = random.randrange(0, self.WIDTH, 40)
                y = random.randrange(0, self.HEIGHT, 40)
                key = f'{x},{y}'
                if key not in self.init_pos:
                    break
    
            self.agents[key] = Agent(x, y)
            self.agents[key].type = agent
            print(f'Key: {key} Agent: {self.agents[key]}')
        

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
            # TODO
            # Add agent.setTarget
            # Add agent.target
            # Add agent.update
            pass

        for coin in self.coins:
            for _, agent in self.agents.items():
                if agent.x == coin.x and agent.y == coin.y:
                    print("yay a coin")

    def on_render(self):
        # Render background
        self._display_surf.fill(BLACK)

        # Render coins
        for coin in self.coins:
            coin.draw(self._display_surf)

        # Render agents
        for agent in self.agents.values():
            agent.draw(self._display_surf, agent._surface)
        
        # i=1
        # for agent in self.agents.values():
        #     agent.show_score(self._display_surf, i, self.WIDTH, self.HEIGHT, WHITE, self.font)
        #     i+=1

        pg.display.flip()

    def _run(self):
        # Check for init failure
        if self.on_init() == False:
            self._running = False
        
        # Main game loop
        while self._running:
            # Check if user quits
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self._running = False
            pg.event.pump()
            self.on_loop()
            self.on_render()
            time.sleep(50.0 / 1000.0)

        # Actions after game ends
        print("Game over")
        self.on_cleanup()

    def __str__(self) -> str:
        return f'Game dimensions: {self.WIDTH} x {self.HEIGHT}'

    
        


